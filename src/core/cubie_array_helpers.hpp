#ifndef CUBIE_ARRAY_HELPERS_HPP
#define CUBIE_ARRAY_HELPERS_HPP

#include <array>
#include <cstdint>

namespace rubiks {

// Helper struct to mirror the array representation from the Python reference
struct CubieArrayState {
    std::array<uint8_t, 8> cp; // Corner Permutation
    std::array<uint8_t, 8> co; // Corner Orientation
    std::array<uint8_t, 12> ep; // Edge Permutation
    std::array<uint8_t, 12> eo; // Edge Orientation
};

// Function to apply a move defined by permutations to an array state.
// This logic is ported directly from Hkociemba's cubie.py `corner_multiply` and `edge_multiply`.
void apply_move_to_array(CubieArrayState& state, const CubieArrayState& move);

} // namespace rubiks

#endif // CUBIE_ARRAY_HELPERS_HPP
