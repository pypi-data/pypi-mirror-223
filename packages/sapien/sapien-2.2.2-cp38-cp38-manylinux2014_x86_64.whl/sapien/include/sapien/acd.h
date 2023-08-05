#pragma once
#include <memory>
#include <vector>
#include <coacd.h>

namespace sapien {
class SNonconvexMeshGeometry;
class SConvexMeshGeometry;

std::vector<std::shared_ptr<SConvexMeshGeometry>>
CoACD(std::shared_ptr<SNonconvexMeshGeometry> g,
      double threshold = 0.05,        // concavity stop criterion (0.05)
      bool preprocess = true,         // run manifold algorithm as preprocess (true)
      int preprocess_resolution = 30, // preprocess resolution (30)
      bool pca = false,               // PCA (false)
      bool merge = true,              // merge convex hull after decomposition
      int mcts_max_depth = 3, int mcts_nodes = 20, int mcts_iteration = 150,
      unsigned int seed = 0);

}; // namespace sapien
