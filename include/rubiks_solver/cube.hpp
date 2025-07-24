#ifndef RUBIKS_SOLVER_CUBE_HPP
#define RUBIKS_SOLVER_CUBE_HPP

// Public interface for the Rubik's Cube solver
#include "../../src/core/cube.hpp"

namespace rubiks {

// Re-export main classes for public API
using Cube = rubiks::Cube;
using Move = rubiks::Move;

// Convenience functions
Cube create_scrambled_cube(const std::string& scramble);
bool solve_cube(const Cube& scrambled, std::vector<int>& solution);

} // namespace rubiks

#endif // RUBIKS_SOLVER_CUBE_HPP
