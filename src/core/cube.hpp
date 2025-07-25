#ifndef RUBIKS_CUBE_HPP
#define RUBIKS_CUBE_HPP

#include <cstdint>
#include <string>
#include <vector>
#include <array>

namespace rubiks {

// Forward declaration for move constants
enum Move : int;

class Cube {
public:
    // Bitboard representation: 64-bit for corners, 64-bit for edges
    // Corner packing: 8 corners, 5 bits each (3 for position, 2 for orientation) = 40 bits
    // Edge packing: 12 edges, 5 bits each (4 for position, 1 for orientation) = 60 bits
    struct State {
        uint64_t corners;
        uint64_t edges;

        bool operator==(const State& other) const {
            return corners == other.corners && edges == other.edges;
        }
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

    // Utility
    std::string to_string() const;
    uint64_t hash() const;

private:
    State state_;
    
    // The solved state is defined as identity permutation and zero orientation, which is 0.
    static const uint64_t SOLVED_CORNERS = 0ULL;
    static const uint64_t SOLVED_EDGES = 0ULL;
    
    // This static initialization ensures move tables are generated only once.
    static void initialize_move_tables();
    static bool tables_initialized;
};

// Move constants (scoped enum for type safety)
enum Move : int {
    U1 = 0, U2, U3,
    R1, R2, R3,
    F1, F2, F3,
    D1, D2, D3,
    L1, L2, L3,
    B1, B2, B3,
    NUM_MOVES = 18
};

// Aliases for standard notation for convenience in C++ code
constexpr Move U = U1, U_PRIME = U3;
constexpr Move R = R1, R_PRIME = R3;
constexpr Move F = F1, F_PRIME = F3;
constexpr Move D = D1, D_PRIME = D3;
constexpr Move L = L1, L_PRIME = L3;
constexpr Move B = B1, B_PRIME = B3;

} // namespace rubiks

#endif // RUBIKS_CUBE_HPP
