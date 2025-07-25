// FILE: src/pdb/pattern_db.cpp
// ACTION: Replace the entire file with this content.

#include "pattern_db.hpp"
#include <fstream>
#include <iostream>
#include <queue>
#include <vector>
#include <array>
#include "../core/cube.hpp" // For Move enum

// Include lz4.h if you have the library installed
// #include <lz4.h>

namespace rubiks {

// Helper struct to mirror the array representation from the Python reference
// This is used ONLY during the one-time initialization of move tables.
struct CubieArrayState {
    std::array<uint8_t, 8> cp; // Corner Permutation
    std::array<uint8_t, 8> co; // Corner Orientation
    std::array<uint8_t, 12> ep; // Edge Permutation
    std::array<uint8_t, 12> eo; // Edge Orientation
};

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

// Helper: Convert corner orientation array to a unique integer index (0-2186)
// This logic is ported from Hkociemba's get_twist().
uint16_t corner_orientations_to_index(const std::array<uint8_t, 8>& co) {
    uint16_t index = 0;
    for (int i = 0; i < 7; ++i) {
        index = index * 3 + co[i];
    }
    return index;
}

// Helper: Convert index back to corner orientation array
std::array<uint8_t, 8> index_to_corner_orientations(uint16_t index) {
    std::array<uint8_t, 8> co;
    int orientation_sum = 0;
    for (int i = 6; i >= 0; --i) {
        co[i] = index % 3;
        orientation_sum += co[i];
        index /= 3;
    }
    co[7] = (3 - (orientation_sum % 3)) % 3;
    return co;
}

PatternDB::PatternDB(const std::string& filename) {
    if (!load_from_file(filename)) {
        std::cout << "PDB file not found. Building " << filename << "..." << std::endl;
        PatternDBBuilder::build_corner_orientation_pdb(filename);
        if (!load_from_file(filename)) {
            std::cerr << "FATAL: Failed to build and load PDB." << std::endl;
        }
    }
}

PatternDB::~PatternDB() = default;

bool PatternDB::load_from_file(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    if (!file.is_open()) {
        return false;
    }

    // TODO: Implement LZ4 decompression here.
    // For now, we read the raw, uncompressed data.
    file.seekg(0, std::ios::end);
    size_t size = file.tellg();
    file.seekg(0, std::ios::beg);

    entries_.resize(size);
    file.read(reinterpret_cast<char*>(entries_.data()), size);
    file.close();

    std::cout << "✓ Successfully loaded PDB: " << filename << " (" << size << " entries)" << std::endl;
    return true;
}

uint8_t PatternDB::lookup(const Cube::State& state) const {
    // This lookup needs to extract the pattern from the bitboard state.
    // This is a complex step. For this PDB, we need the corner orientations.
    std::array<uint8_t, 8> co;
    uint64_t corner_data = state.corners;
    for (int i = 7; i >= 0; --i) {
        co[i] = corner_data & 0b11; // Extract 2 bits of orientation
        corner_data >>= 5;
    }
    uint16_t index = corner_orientations_to_index(co);
    return entries_[index];
}

void PatternDBBuilder::build_corner_orientation_pdb(const std::string& output_file) {
    const int NUM_STATES = 2187; // 3^7
    std::cout << "Building corner orientation PDB (" << NUM_STATES << " states)..." << std::endl;

    // Step 1: Generate the move table for corner orientations (the "twist" coordinate)
    std::vector<std::vector<uint16_t>> move_table(NUM_STATES, std::vector<uint16_t>(NUM_MOVES));
    
    // Ported logic from cubie.py and moves.py to generate this table
    std::array<CubieArrayState, 6> basic_moves;
    // (Same move definitions as in cube.cpp)
    basic_moves[0] = {{4, 5, 6, 7, 3, 0, 1, 2}, {0,0,0,0,0,0,0,0}, {3,0,1,2,4,5,6,7,8,9,10,11}, {0,0,0,0,0,0,0,0,0,0,0,0}};
    basic_moves[1] = {{3, 1, 2, 7, 0, 5, 6, 4}, {1,0,0,2,2,0,0,1}, {8, 1, 2, 0, 11, 5, 6, 7, 4, 9, 10, 3}, {0,0,0,0,0,0,0,0,0,0,0,0}};
    basic_moves[2] = {{1, 5, 2, 3, 0, 4, 6, 7}, {2,1,0,0,1,2,0,0}, {0, 9, 2, 3, 4, 8, 6, 7, 1, 5, 10, 11}, {0,1,0,0,0,1,0,0,1,1,0,0}};
    basic_moves[3] = {{0, 1, 2, 3, 5, 6, 7, 4}, {0,0,0,0,0,0,0,0}, {0,1,2,3,5,6,7,4,8,9,10,11}, {0,0,0,0,0,0,0,0,0,0,0,0}};
    basic_moves[4] = {{0, 2, 6, 3, 4, 1, 5, 7}, {0,2,1,0,0,1,2,0}, {0,1,10,3,4,5,9,7,8,2,6,11}, {0,0,0,0,0,0,0,0,0,0,0,0}};
    basic_moves[5] = {{0, 1, 3, 7, 4, 5, 2, 6}, {0,0,2,1,0,0,1,2}, {0,1,2,11,4,5,6,10,8,9,3,7}, {0,0,0,1,0,0,0,1,0,0,1,1}};

    for (uint16_t i = 0; i < NUM_STATES; ++i) {
        CubieArrayState state = { {}, index_to_corner_orientations(i), {}, {} };
        for(int j=0; j<8; ++j) state.cp[j] = j; // Permutation doesn't matter for this PDB

        CubieArrayState temp_state = state;
        for (int move_idx = 0; move_idx < 6; ++move_idx) {
            for (int pow = 0; pow < 3; ++pow) {
                apply_move_to_array(temp_state, basic_moves[move_idx]);
                move_table[i][move_idx * 3 + pow] = corner_orientations_to_index(temp_state.co);
            }
            apply_move_to_array(temp_state, basic_moves[move_idx]); // fourth move to restore
        }
    }
    std::cout << "✓ Move table for PDB generation complete." << std::endl;

    // Step 2: Perform BFS to calculate distances
    std::vector<uint8_t> distances(NUM_STATES, 255);
    std::queue<uint16_t> q;

    distances[0] = 0;
    q.push(0);

    int count = 1;
    while (!q.empty()) {
        uint16_t current_state = q.front();
        q.pop();

        uint8_t dist = distances[current_state];

        for (int move = 0; move < NUM_MOVES; ++move) {
            uint16_t next_state = move_table[current_state][move];
            if (distances[next_state] == 255) {
                distances[next_state] = dist + 1;
                q.push(next_state);
                count++;
            }
        }
    }
    std::cout << "✓ BFS complete. " << count << " states reached." << std::endl;

    // Step 3: Save the PDB to a file
    // TODO: Implement LZ4 compression here
    // const int max_compressed_size = LZ4_compressBound(NUM_STATES);
    // std::vector<char> compressed_data(max_compressed_size);
    // const int compressed_size = LZ4_compress_default(
    //      reinterpret_cast<const char*>(distances.data()), 
    //      compressed_data.data(), 
    //      NUM_STATES, 
    //      max_compressed_size);
    
    std::ofstream file(output_file, std::ios::binary);
    // file.write(compressed_data.data(), compressed_size);
    file.write(reinterpret_cast<const char*>(distances.data()), NUM_STATES);
    file.close();

    std::cout << "✓ PDB saved to " << output_file << std::endl;
}

} // namespace rubiks
    return static_cast<double>(uncompressed_size_) / compressed_size_;
}

uint64_t PatternDB::compute_pattern_key(uint64_t state) const {
    // Simple hash function for pattern extraction
    return state ^ (state >> 32);
}

// PatternDBBuilder implementation
void PatternDBBuilder::build_corner_pdb(const std::string& output_file) {
    std::cout << "Building corner pattern database..." << std::endl;
    bfs_build(output_file, true);
}

void PatternDBBuilder::build_edge_pdb(const std::string& output_file) {
    std::cout << "Building edge pattern database..." << std::endl;
    bfs_build(output_file, false);
}

void PatternDBBuilder::bfs_build(const std::string& output_file, bool is_corner_db) {
    // Placeholder BFS implementation
    std::ofstream file(output_file, std::ios::binary);
    if (!file.is_open()) {
        std::cerr << "Could not create output file: " << output_file << std::endl;
        return;
    }
    
    // Generate simple pattern database
    const size_t db_size = 1000000;
    std::vector<uint8_t> db(db_size);
    
    for (size_t i = 0; i < db_size; ++i) {
        db[i] = static_cast<uint8_t>(i % 20);
    }
    
    file.write(reinterpret_cast<const char*>(db.data()), db.size());
    file.close();
    
    std::cout << "Pattern database built: " << output_file << std::endl;
}

} // namespace rubiks
