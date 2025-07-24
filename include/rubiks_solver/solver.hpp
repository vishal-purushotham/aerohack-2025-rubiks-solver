#ifndef RUBIKS_SOLVER_HPP
#define RUBIKS_SOLVER_HPP

#include "cube.hpp"
#include "../../src/core/moves.hpp"
#include "../../src/pdb/pattern_db.hpp"
#include <vector>
#include <string>

namespace rubiks {

class RubiksSolver {
public:
    RubiksSolver();
    ~RubiksSolver();
    
    // Solve a scrambled cube
    std::vector<int> solve(const Cube& scrambled_cube);
    std::vector<int> solve(const std::string& scramble);
    
    // Configuration
    void set_max_depth(int depth) { max_depth_ = depth; }
    void set_use_gpu(bool use_gpu) { use_gpu_ = use_gpu; }
    void set_beam_width(int width) { beam_width_ = width; }
    
    // Statistics
    int get_nodes_explored() const { return nodes_explored_; }
    double get_solve_time() const { return solve_time_; }
    
private:
    int max_depth_;
    bool use_gpu_;
    int beam_width_;
    int nodes_explored_;
    double solve_time_;
    
    PatternDB* corner_db_;
    PatternDB* edge_db_;
    
    // Search algorithms
    std::vector<int> ida_star_search(const Cube& cube);
    std::vector<int> beam_search(const Cube& cube);
    
    // Heuristics
    int compute_heuristic(const Cube& cube);
};

// Utility functions
namespace solver {
    std::string moves_to_notation(const std::vector<int>& moves);
    std::vector<int> notation_to_moves(const std::string& notation);
    bool verify_solution(const std::string& scramble, const std::vector<int>& solution);
}

} // namespace rubiks

#endif // RUBIKS_SOLVER_HPP
