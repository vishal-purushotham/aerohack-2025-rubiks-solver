#ifndef RUBIKS_CUBE_HPP
#define RUBIKS_CUBE_HPP

#include <cstdint>
#include <string>
#include <vector>

namespace rubiks {

class Cube {
public:
    // Bitboard representation: 64-bit for corners, 64-bit for edges
    struct State {
        uint64_t corners;
        uint64_t edges;
    };

    Cube();
    explicit Cube(const std::string& scramble);
    
    // Core operations
    void apply_move(int move_id);
    void apply_scramble(const std::string& scramble);
    bool is_solved() const;
    
    // State access
    State get_state() const { return state_; }
    void set_state(const State& state) { state_ = state; }
    
    // Move generation
    std::vector<int> get_valid_moves() const;
    
    // Utility
    std::string to_string() const;
    uint64_t hash() const;
    
private:
    State state_;
    static const uint64_t SOLVED_CORNERS = 0x0123456789ABCDEFULL;
    static const uint64_t SOLVED_EDGES = 0x0123456789ABCDEFULL;
    
    void initialize_move_tables();
};

// Move constants
enum Move {
    R = 0, R_PRIME, R2,
    L, L_PRIME, L2,
    U, U_PRIME, U2,
    D, D_PRIME, D2,
    F, F_PRIME, F2,
    B, B_PRIME, B2,
    NUM_MOVES = 18
};

} // namespace rubiks

#endif // RUBIKS_CUBE_HPP
