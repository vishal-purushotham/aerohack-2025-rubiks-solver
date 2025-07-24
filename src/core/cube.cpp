#include "cube.hpp"
#include <sstream>
#include <random>
#include <unordered_map>

namespace rubiks {

// Move lookup tables - pre-computed XOR deltas for each move
static uint64_t corner_deltas[NUM_MOVES];
static uint64_t edge_deltas[NUM_MOVES];
static bool tables_initialized = false;

Cube::Cube() : state_{SOLVED_CORNERS, SOLVED_EDGES} {
    if (!tables_initialized) {
        initialize_move_tables();
        tables_initialized = true;
    }
}

Cube::Cube(const std::string& scramble) : Cube() {
    apply_scramble(scramble);
}

void Cube::apply_move(int move_id) {
    if (move_id >= 0 && move_id < NUM_MOVES) {
        state_.corners ^= corner_deltas[move_id];
        state_.edges ^= edge_deltas[move_id];
    }
}

void Cube::apply_scramble(const std::string& scramble) {
    std::istringstream iss(scramble);
    std::string move;
    
    // Simple move mapping
    std::unordered_map<std::string, int> move_map = {
        {"R", R}, {"R'", R_PRIME}, {"R2", R2},
        {"L", L}, {"L'", L_PRIME}, {"L2", L2},
        {"U", U}, {"U'", U_PRIME}, {"U2", U2},
        {"D", D}, {"D'", D_PRIME}, {"D2", D2},
        {"F", F}, {"F'", F_PRIME}, {"F2", F2},
        {"B", B}, {"B'", B_PRIME}, {"B2", B2}
    };
    
    while (iss >> move) {
        auto it = move_map.find(move);
        if (it != move_map.end()) {
            apply_move(it->second);
        }
    }
}

bool Cube::is_solved() const {
    return state_.corners == SOLVED_CORNERS && state_.edges == SOLVED_EDGES;
}

std::vector<int> Cube::get_valid_moves() const {
    std::vector<int> moves;
    for (int i = 0; i < NUM_MOVES; ++i) {
        moves.push_back(i);
    }
    return moves;
}

std::string Cube::to_string() const {
    // Simple string representation
    return "Cube[corners=" + std::to_string(state_.corners) + 
           ",edges=" + std::to_string(state_.edges) + "]";
}

void Cube::initialize_move_tables() {
    // Initialize with placeholder values - these should be computed properly
    // For now, using simple non-zero values to make moves detectable
    
    // R moves
    corner_deltas[R] = 0x1000000000000000ULL;
    edge_deltas[R] = 0x0100000000000000ULL;
    corner_deltas[R_PRIME] = 0x2000000000000000ULL;
    edge_deltas[R_PRIME] = 0x0200000000000000ULL;
    corner_deltas[R2] = 0x3000000000000000ULL;
    edge_deltas[R2] = 0x0300000000000000ULL;
    
    // L moves
    corner_deltas[L] = 0x0100000000000000ULL;
    edge_deltas[L] = 0x0010000000000000ULL;
    corner_deltas[L_PRIME] = 0x0200000000000000ULL;
    edge_deltas[L_PRIME] = 0x0020000000000000ULL;
    corner_deltas[L2] = 0x0300000000000000ULL;
    edge_deltas[L2] = 0x0030000000000000ULL;
    
    // U moves
    corner_deltas[U] = 0x0010000000000000ULL;
    edge_deltas[U] = 0x0001000000000000ULL;
    corner_deltas[U_PRIME] = 0x0020000000000000ULL;
    edge_deltas[U_PRIME] = 0x0002000000000000ULL;
    corner_deltas[U2] = 0x0030000000000000ULL;
    edge_deltas[U2] = 0x0003000000000000ULL;
    
    // D moves
    corner_deltas[D] = 0x0001000000000000ULL;
    edge_deltas[D] = 0x0000100000000000ULL;
    corner_deltas[D_PRIME] = 0x0002000000000000ULL;
    edge_deltas[D_PRIME] = 0x0000200000000000ULL;
    corner_deltas[D2] = 0x0003000000000000ULL;
    edge_deltas[D2] = 0x0000300000000000ULL;
    
    // F moves
    corner_deltas[F] = 0x0000100000000000ULL;
    edge_deltas[F] = 0x0000010000000000ULL;
    corner_deltas[F_PRIME] = 0x0000200000000000ULL;
    edge_deltas[F_PRIME] = 0x0000020000000000ULL;
    corner_deltas[F2] = 0x0000300000000000ULL;
    edge_deltas[F2] = 0x0000030000000000ULL;
    
    // B moves
    corner_deltas[B] = 0x0000010000000000ULL;
    edge_deltas[B] = 0x0000001000000000ULL;
    corner_deltas[B_PRIME] = 0x0000020000000000ULL;
    edge_deltas[B_PRIME] = 0x0000002000000000ULL;
    corner_deltas[B2] = 0x0000030000000000ULL;
    edge_deltas[B2] = 0x0000003000000000ULL;
}

uint64_t Cube::hash() const {
    return state_.corners ^ (state_.edges << 1);
}

} // namespace rubiks
