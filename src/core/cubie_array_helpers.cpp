#include "cubie_array_helpers.hpp"

namespace rubiks {

// Function to apply a move defined by permutations to an array state.
// This logic is ported directly from Hkociemba's cubie.py `corner_multiply` and `edge_multiply`.
void apply_move_to_array(CubieArrayState& state, const CubieArrayState& move) {
    CubieArrayState old_state = state;
    // Apply corner move
    for (int i = 0; i < 8; ++i) {
        state.cp[i] = old_state.cp[move.cp[i]];
        state.co[i] = (old_state.co[move.cp[i]] + move.co[i]) % 3;
    }
    // Apply edge move
    for (int i = 0; i < 12; ++i) {
        state.ep[i] = old_state.ep[move.ep[i]];
        state.eo[i] = (old_state.eo[move.ep[i]] + move.eo[i]) % 2;
    }
}

} // namespace rubiks
