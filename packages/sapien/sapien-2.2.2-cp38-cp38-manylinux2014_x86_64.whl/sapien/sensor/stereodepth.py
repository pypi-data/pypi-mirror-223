from ..core import (
    Pose,
    Scene,
    Actor
)
from ..core.pysapien.simsense import DepthSensorEngine
from .sensor_base import SensorEntity
from typing import Optional
from copy import deepcopy as copy

import os
import numpy as np
import cv2


class StereoDepthSensorConfig:
    """
    An instance of this class is required to initialize StereoDepthSensor.
    """

    def __init__(self):
        self.light_pattern = os.path.join(os.path.dirname(__file__), 'assets/patterns/d415.png')
        """Path to active light pattern file. Use RGB modality if set to None."""

        self.ir_ambient_strength = 0.002
        """Strength of the active light."""

        self.ir_light_dim_factor = 0.05
        """Final light strength will be timed by ir_light_dim_factor."""

        self.rgb_resolution = (1920, 1080)
        """Resolution of the RGB camera (width x height)."""

        self.ir_resolution = (1280, 720)
        """Resolution of the infrared cameras (width x height)."""

        self.rgb_intrinsic = np.array([
            [1380.,    0., 960.],
            [0.,    1380., 540.],
            [0.,       0.,   1.]
        ])
        """Intrinsic matrix of the RGB camera."""

        self.ir_intrinsic = np.array([
            [920.,   0., 640.],
            [0.,   920., 360.],
            [0.,     0.,   1.]
        ])
        """Intrinsic matrix of the infrared cameras."""

        self.trans_pose_l = Pose([0, -0.0175, 0])
        """Relative pose of the left infrared camera to the RGB camera."""

        self.trans_pose_r = Pose([0, -0.0720, 0])
        """Relative pose of the right infrared camera to the RGB camera."""

        self.min_depth = 0.2
        """Minimum valid depth in meters."""

        self.max_depth = 10.0
        """Maximum valid depth (non-inclusive) in meters."""

        self.ir_noise_seed = 0
        """Random seed for simulating infrared noise."""
        
        self.ir_speckle_noise = 1.0
        """Scale for simulating infrared speckle noise. Set to 0 will disable noise simulation."""

        self.ir_thermal_noise = 1.0
        """Scale for simulating infrared thermal noise. Only effective when speckle noise is on."""

        self.rectified = True
        """Set to true if left and right infrared cameras have a common image plane,
        otherwise false."""

        self.census_width = 7
        """Width of the center-symmetric census transform window for steoreo matching.
        This must be an odd number."""

        self.census_height = 7
        """Height of the center-symmetric census transform window for stereo matching.
        This must be an odd number."""

        self.max_disp = 128
        """Maximum disparity (non-inclusive) for stereo matching."""

        self.block_width = 7
        """Width of the matched block for stereo matching. This must be an odd number."""

        self.block_height = 7
        """Height of the matched block for stereo matching. This must be an odd number."""

        self.p1_penalty = 8
        """P1 penalty for semi-global matching algorithm."""

        self.p2_penalty = 32
        """P2 penalty for semi-global matching algorithm."""

        self.uniqueness_ratio = 15
        """How much (in percentage) the minimum cost computed in stereo matching must exceed
        the second best cost (ignoring best match's adjacent pixels) to be considered valid."""

        self.lr_max_diff = 1
        """Maximum allowed difference of the left-right consistency check in stereo matching.
        Set it to 255 will disable the check."""

        self.median_filter_size = 3
        """Size of the median filter for disparity post-processing. Choices are 1, 3, 5, 7.
        Set to 1 will disable median filter."""

        self.depth_dilation = True
        """Final depth will be transformed into the same size of rgb_resolution, and depth dilation
        can dilate the final depth map to avoid holes. Recommended to set as true if rgb_resolution
        is greater than ir_resolution."""


class StereoDepthSensor(SensorEntity):
    """
    This class simulates an active stereo depth sensor. It has one RGB camera and two infrared camera.
    Depth is computed via semi-global block matching. Refer to StereoDepthSensorConfig for configurable
    parameters. The computed depth map will be presented in RGB camera frame.
    """

    def __init__(self, sensor_name: str, scene: Scene, config: StereoDepthSensorConfig, mount: Optional[Actor] = None, pose: Optional[Pose] = None):
        """
        :param sensor_name: name of the sensor.
        :param scene: scene that the sensor is attached to.
        :param config: configuration of the sensor.
        :param mount: optionally mount the sensor to an actor. If mounted, the sensor will move along with the actor.
        :param pose: If not mounted, this will be the global pose for the sensor. Otherwise, it will be the local pose relative to the mounted actor.
        """
  
        super().__init__()

        # Basic configuration
        self.name = sensor_name
        self._scene = scene
        self._config = config

        # Instance check
        if not isinstance(self._config.rgb_resolution[0], int) or not isinstance(self._config.rgb_resolution[1], int):
            raise TypeError("RGB resolution (width and height) must be integer")

        if not isinstance(self._config.ir_resolution[0], int) or not isinstance(self._config.ir_resolution[1], int) or \
            self._config.ir_resolution[0] < 32 or self._config.ir_resolution[1] < 32:
            raise TypeError("Infrared resolution (width and height) must be integer and no less than 32")

        if self._config.ir_speckle_noise > 0 and self._config.ir_thermal_noise <= 0:
            raise TypeError("ir_speckle_noise > 0, Infrared noise simulation is on. ir_thermal_noise must also be positive")
        
        if not isinstance(self._config.census_width, int) or not isinstance(self._config.census_height, int) or \
            self._config.census_width <= 0 or self._config.census_height <= 0 or \
            self._config.census_width % 2 == 0 or self._config.census_height % 2 == 0 or \
            self._config.census_width * self._config.census_height > 65:
            raise TypeError("census_width and census_height must be positive odd integers and their product should be no larger than 65")
        
        if not isinstance(self._config.max_disp, int) or self._config.max_disp < 32 or self._config.max_disp > 1024:
            raise TypeError("max_disp must be integer and within range [32, 1024]")
        
        if not isinstance(self._config.block_width, int) or not isinstance(self._config.block_height, int) or \
            self._config.block_width <= 0 or self._config.block_height <= 0 or \
            self._config.block_width % 2 == 0 or self._config.block_height % 2 == 0 or \
            self._config.block_width * self._config.block_height > 256:
            raise TypeError("block_width and block_height must be positive odd integers and their product should be no larger than 256")
 
        if not isinstance(self._config.p1_penalty, int) or not isinstance(self._config.p2_penalty, int) or self._config.p1_penalty <= 0 or \
            self._config.p2_penalty <= 0 or self._config.p1_penalty >= self._config.p2_penalty or self._config.p2_penalty >= 224:
            raise TypeError("p1_penalty must be positive integer less than p2_penalty and p2_penalty be positive integer less than 224")

        if not isinstance(self._config.uniqueness_ratio, int) or self._config.uniqueness_ratio < 0 or self._config.uniqueness_ratio > 255:
            raise TypeError("uniqueness_ratio must be positive integer and no larger than 255")

        if not isinstance(self._config.lr_max_diff, int) or self._config.lr_max_diff < -1 or self._config.lr_max_diff > 255:
            raise TypeError("lr_max_diff must be integer and within the range [0, 255]")

        if self._config.median_filter_size != 1 and self._config.median_filter_size != 3 and self._config.median_filter_size != 5 and \
            self._config.median_filter_size != 7:
            raise TypeError("Median filter size choices are 1, 3, 5, 7")

        # self._pose is global if not mounted and local if mounted
        self._mount = mount
        if pose is None:
            self._pose = Pose()
        else:
            self._pose = pose

        # Active Light
        self._alight = self._scene.add_active_light(
            pose=Pose(), color=[0, 0, 0], fov=1.57, tex_path=self._config.light_pattern)
        if self._mount is not None:
            self._alight.set_parent(self._mount, keep_pose=False)
        self._alight.set_local_pose(self._pose)
        
        # Cameras
        self._cam_rgb = None
        self._cam_ir_l = None
        self._cam_ir_r = None
        self._create_cameras()

        # Noise simulation parameters
        self._default_speckle_shape = 1333.33
        self._default_gaussian_sigma = 0.25
        self._default_gaussian_mu = 0
        if self._config.ir_speckle_noise == 0:
            speckle_shape = 0
        else:
            speckle_shape = self._default_speckle_shape / self._config.ir_speckle_noise
        speckle_scale = self._config.ir_speckle_noise / self._default_speckle_shape
        gaussian_mu = self._default_gaussian_mu
        gaussian_sigma = self._default_gaussian_sigma * self._config.ir_thermal_noise

        # Depth computing engine
        ir_size, rgb_size = self._config.ir_resolution, self._config.rgb_resolution
        ir_intrinsic = self._config.ir_intrinsic.astype(float)
        rgb_intrinsic = self._config.rgb_intrinsic.astype(float)
        rgb_pose = self._cam_rgb.get_pose()
        rgb_extrinsic = self._pose2cv2ex(rgb_pose)
        l_extrinsic = self._pose2cv2ex(rgb_pose * self._config.trans_pose_l)
        r_extrinsic = self._pose2cv2ex(rgb_pose * self._config.trans_pose_r)
        l2r = r_extrinsic @ np.linalg.inv(l_extrinsic).astype(float)
        l2rgb = rgb_extrinsic @ np.linalg.inv(l_extrinsic).astype(float)
        r1, r2, p1, p2, q, _, _ = cv2.stereoRectify(
            cameraMatrix1=ir_intrinsic, distCoeffs1=None, cameraMatrix2=ir_intrinsic, distCoeffs2=None,
            imageSize=ir_size, R=l2r[:3, :3], T=l2r[:3, 3:], alpha=1.0, newImageSize=ir_size
        )
        f_len = q[2][3] # focal length of the left camera in meters
        b_len = 1.0 / q[3][2] # baseline length in meters
        map_l = cv2.initUndistortRectifyMap(ir_intrinsic, None, r1, p1, ir_size, cv2.CV_32F)
        map_r = cv2.initUndistortRectifyMap(ir_intrinsic, None, r2, p2, ir_size, cv2.CV_32F)
        map_lx, map_ly = map_l
        map_rx, map_ry = map_r
        a1, a2, a3, b = self._get_registration_mat(ir_size, ir_intrinsic, rgb_intrinsic, l2rgb)
        rgb_fx = rgb_intrinsic[0][0]
        rgb_fy = rgb_intrinsic[1][1]
        rgb_skew = rgb_intrinsic[0][1]
        rgb_cx = rgb_intrinsic[0][2]
        rgb_cy = rgb_intrinsic[1][2]

        self._engine = DepthSensorEngine(
            ir_size[1], ir_size[0], rgb_size[1], rgb_size[0], f_len, b_len, self._config.min_depth, self._config.max_depth,
            self._config.ir_noise_seed, speckle_shape, speckle_scale, gaussian_mu, gaussian_sigma, self._config.rectified,
            self._config.census_width, self._config.census_height, self._config.max_disp, self._config.block_width,
            self._config.block_height, self._config.p1_penalty, self._config.p2_penalty, self._config.uniqueness_ratio,
            self._config.lr_max_diff, self._config.median_filter_size, map_lx, map_ly, map_rx, map_ry, a1, a2, a3, b[0],
            b[1], b[2], self._config.depth_dilation, rgb_fx, rgb_fy, rgb_skew, rgb_cx, rgb_cy
        )

    def take_picture(self, infrared_only: bool = False):
        """
        Note: We expect one scene.update_render() call before calling take_picture().

        :param infrared_only: If true, only take infrared pictures without taking RGB picture.
        """
        if not infrared_only:
            self._cam_rgb.take_picture()
        self._ir_mode()
        self._scene.update_render()
        self._cam_ir_l.take_picture()
        self._cam_ir_r.take_picture()
        self._normal_mode()
        self._scene.update_render()
    
    def compute_depth(self):
        left_dl_tensor = self._cam_ir_l.get_dl_tensor('Color')
        right_dl_tensor = self._cam_ir_r.get_dl_tensor('Color')
        self._engine.compute(left_dl_tensor, right_dl_tensor)

    def set_pose(self, pose: Pose):
        """
        Set the global pose of the sensor. Call set_local_pose instead of set_pose if mount exists.
        """
        if self._mount is None:
            self._pose = pose
            self._alight.set_pose(pose)
            self._cam_rgb.set_local_pose(pose)
            self._cam_ir_l.set_local_pose(pose * self._config.trans_pose_l)
            self._cam_ir_r.set_local_pose(pose * self._config.trans_pose_r)
        else:
            raise RuntimeError("cannot set_pose when sensor is mounted, use set_local_pose instead")

    def set_local_pose(self, pose: Pose):
        """
        If mount exists, set local pose of the sensor relative to mounted actor. Otherwise, set global pose of the sensor.
        """
        self._pose = pose
        self._alight.set_local_pose(pose)
        self._cam_rgb.set_local_pose(pose)
        self._cam_ir_l.set_local_pose(pose * self._config.trans_pose_l)
        self._cam_ir_r.set_local_pose(pose * self._config.trans_pose_r)
    
    def set_ir_noise(self, ir_speckle_noise: float, ir_thermal_noise: float):
        """
        :param ir_speckle_noise: Scale for simulating infrared speckle noise. Set to 0 will disable noise simulation.
        :param ir_thermal_noise: Scale for simulating infrared thermal noise. Only effective when speckle noise is on.
        """
        if ir_speckle_noise > 0 and ir_thermal_noise <= 0:
            raise TypeError("ir_speckle_noise > 0, Infrared noise simulation is on. ir_thermal_noise must also be positive")
        if ir_speckle_noise == 0:
            speckle_shape = 0
        else:
            speckle_shape = self._default_speckle_shape / ir_speckle_noise
        speckle_scale = ir_speckle_noise / self._default_speckle_shape
        gaussian_mu = self._default_gaussian_mu
        gaussian_sigma = self._default_gaussian_sigma * ir_thermal_noise

        self._config.ir_speckle_noise = ir_speckle_noise
        self._config.ir_thermal_noise = ir_thermal_noise
        self._engine.set_ir_noise_parameters(speckle_shape, speckle_scale, gaussian_mu, gaussian_sigma)
    
    def set_census_window_size(self, census_width: int, census_height: int):
        """
        :param census_width: Width of the center-symmetric census transform window. This must be an odd number.
        :param census_height: Height of the center-symmetric census transform window. This must be an odd number.
        """
        if not isinstance(census_width, int) or not isinstance(census_height, int) or census_width <= 0 or census_height <= 0 or \
            census_width % 2 == 0 or census_height % 2 == 0 or census_width*census_height > 65:
            raise TypeError("census_width and census_height must be positive odd integers and their product should be no larger than 65")
        self._config.census_width = census_width
        self._config.census_height = census_height
        self._engine.set_census_window_size(census_width, census_height)
    
    def set_matching_block_size(self, block_width: int, block_height: int):
        """
        :param block_width: Width of the matched block. This must be an odd number.
        :param block_height: Height of the matched block. This must be an odd number.
        """
        if not isinstance(block_width, int) or not isinstance(block_height, int) or block_width <= 0 or block_height <= 0 or \
            block_width % 2 == 0 or block_height % 2 == 0 or block_width*block_height > 256:
            raise TypeError("block_width and block_height must be positive odd integers and their product should be no larger than 256")
        self._config.block_width = block_width
        self._config.block_height = block_height
        self._engine.set_matching_block_size(block_width, block_height)
    
    def set_penalties(self, p1_penalty: int, p2_penalty: int):
        """
        :param p1_penalty: P1 penalty for semi-global matching algorithm.
        :param p2_penalty: P2 penalty for semi-global matching algorithm.
        """
        if not isinstance(p1_penalty, int) or not isinstance(p2_penalty, int) or p1_penalty <= 0 or p2_penalty <= 0 or \
            p1_penalty >= p2_penalty or p2_penalty >= 224:
            raise TypeError("p1 must be positive integer less than p2 and p2 be positive integer less than 224")
        self._config.p1_penalty = p1_penalty
        self._config.p2_penalty = p2_penalty
        self._engine.set_penalties(p1_penalty, p2_penalty)
    
    def set_uniqueness_ratio(self, uniqueness_ratio: int):
        """
        :param uniqueness_ratio: Margin in percentage by which the minimum computed cost should win the second best (not considering
                                 best match's adjacent pixels) cost to consider the found match valid.
        """
        if not isinstance(uniqueness_ratio, int) or uniqueness_ratio < 0 or uniqueness_ratio > 255:
            raise TypeError("uniqueness_ratio must be positive integer no larger than 255")
        self._config.uniqueness_ratio = uniqueness_ratio
        self._engine.set_uniqueness_ratio(uniqueness_ratio)

    def set_lr_max_diff(self, lr_max_diff: int):
        """
        :param lr_max_diff: Maximum allowed difference in the left-right consistency check. Set it to 255 to disable the check.
        """
        if not isinstance(lr_max_diff, int) or lr_max_diff < -1 or lr_max_diff > 255:
            raise TypeError("lr_max_diff must be integer within the range [0, 255]")
        self._config.lr_max_diff = lr_max_diff
        self._engine.set_lr_max_diff(lr_max_diff)

    def get_config(self):
        return copy(self._config)

    def get_pose(self):
        if self._mount is None:
            return copy(self._pose)
        else:
            return copy(self._mount.get_pose() * self._pose)

    def get_rgb(self):
        rgb = self._cam_rgb.get_color_rgba()[..., :3].clip(0, 1)
        return copy(rgb)

    def get_rgba_dl_tensor(self):
        return self._cam_rgb.get_dl_tensor('Color')

    def get_ir(self):
        """
        Note: Noise simulation won't be reflected here.
        """
        ir_l = self._cam_ir_l.get_color_rgba()[..., 0].clip(0, 1)
        ir_r = self._cam_ir_r.get_color_rgba()[..., 0].clip(0, 1)
        return [copy(ir_l), copy(ir_r)]

    def get_depth(self):
        """
        Note: Returned depth map will be of the same resolution and frame of RGB camera.
        """
        depth = self._engine.get_ndarray()
        return copy(depth)

    def get_depth_dl_tensor(self):
        """
        Note: Returned depth map will be of the same resolution and frame of RGB camera.
        """
        return self._engine.get_dl_tensor()

    def get_pointcloud(self, with_rgb: bool = False):
        """
        Note: Returned point cloud is from RGB camera's with x rightward, y downward, z forward.
        """
        if with_rgb:
            rgba_dl_tensor = self.get_rgba_dl_tensor()
            pc = self._engine.get_rgb_point_cloud_ndarray(rgba_dl_tensor)
        else:
            pc = self._engine.get_point_cloud_ndarray()

        return pc

    def get_pointcloud_dl_tensor(self, with_rgb: bool = False):
        """
        Note: Returned point cloud is from RGB camera's with x rightward, y downward, z forward.
        """
        if with_rgb:
            rgba_dl_tensor = self.get_rgba_dl_tensor()
            pc_dl_tensor = self._engine.get_rgb_point_cloud_dl_tensor(rgba_dl_tensor)
        else:
            pc_dl_tensor = self._engine.get_point_cloud_dl_tensor()

        return pc_dl_tensor

    def _create_cameras(self):
        self._scene.update_render()

        if self._mount is None:
            self._cam_rgb = self._scene.add_camera(
                f"{self.name}", *self._config.rgb_resolution, 0.78, 0.001, 100)
            self._cam_rgb.set_local_pose(self._pose)

            self._cam_ir_l = self._scene.add_camera(
                f"{self.name}_left", *self._config.ir_resolution, 0.78, 0.001, 100)
            self._cam_ir_l.set_local_pose(self._pose * self._config.trans_pose_l)

            self._cam_ir_r = self._scene.add_camera(
                f"{self.name}_right", *self._config.ir_resolution, 0.78, 0.001, 100)
            self._cam_ir_r.set_local_pose(self._pose * self._config.trans_pose_r)
        else:
            self._cam_rgb = self._scene.add_mounted_camera(
                f"{self.name}", self._mount, self._pose, *self._config.rgb_resolution, 0.78, 0.001, 100)

            self._cam_ir_l = self._scene.add_mounted_camera(
                f"{self.name}_left", self._mount, self._pose * self._config.trans_pose_l, *self._config.ir_resolution, 0.78, 0.001, 100)

            self._cam_ir_r = self._scene.add_mounted_camera(
                f"{self.name}_right", self._mount, self._pose * self._config.trans_pose_r, *self._config.ir_resolution, 0.78, 0.001, 100)
        
        self._cam_rgb.set_perspective_parameters(
            0.1, 100.0,
            self._config.rgb_intrinsic[0, 0], self._config.rgb_intrinsic[1, 1],
            self._config.rgb_intrinsic[0, 2], self._config.rgb_intrinsic[1, 2],
            self._config.rgb_intrinsic[0, 1]
        )

        self._cam_ir_l.set_perspective_parameters(
            0.1, 100.0,
            self._config.ir_intrinsic[0, 0], self._config.ir_intrinsic[1, 1],
            self._config.ir_intrinsic[0, 2], self._config.ir_intrinsic[1, 2],
            self._config.ir_intrinsic[0, 1]
        )

        self._cam_ir_r.set_perspective_parameters(
            0.1, 100.0,
            self._config.ir_intrinsic[0, 0], self._config.ir_intrinsic[1, 1],
            self._config.ir_intrinsic[0, 2], self._config.ir_intrinsic[1, 2],
            self._config.ir_intrinsic[0, 1]
        )

    def _ir_mode(self):
        if self._config.light_pattern is None:
            return
        else:
            self._light_d = {}
            for l in self._scene.get_all_lights():
                self._light_d[l] = l.color
                l.set_color(l.color * self._config.ir_light_dim_factor)
            self._light_a = self._scene.ambient_light
            self._scene.set_ambient_light([self._config.ir_ambient_strength, 0, 0])
            self._alight.set_color([1, 0, 0])

    def _normal_mode(self):
        if self._config.light_pattern is None:
            return
        else:
            for l in self._scene.get_all_lights():
                l.set_color(self._light_d[l])
            self._scene.set_ambient_light(self._light_a)
            self._alight.set_color([0, 0, 0])

    @staticmethod
    def _get_registration_mat(ir_size, ir_intrinsic, rgb_intrinsic, ir2rgb):
        R = ir2rgb[:3, :3]
        t = ir2rgb[:3, 3:]
        
        w, h = ir_size
        x = np.arange(w)
        y = np.arange(h)
        u, v = np.meshgrid(x, y)
        w = np.ones_like(u)
        pixel_coords = np.stack([u, v, w], axis=-1) # pixel_coords[y, x] is (x, y, 1)

        A = np.einsum("ij,hwj->hwi", rgb_intrinsic @ R @ np.linalg.inv(ir_intrinsic), pixel_coords)
        B = rgb_intrinsic @ t

        return A[..., 0], A[..., 1], A[..., 2], B

    @staticmethod
    def _pose2cv2ex(pose):
        ros2opencv = np.array([[0., -1., 0., 0.],
                               [0., 0., -1., 0.],
                               [1., 0., 0., 0.],
                               [0., 0., 0., 1.]], dtype=float)
        return ros2opencv @ np.linalg.inv(pose.to_transformation_matrix())
