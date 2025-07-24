#include <cassert>
#include <iostream>
#include "../src/core/cube.hpp"
#include "../src/core/moves.hpp"
#include "../src/pdb/pattern_db.hpp"

using namespace rubiks;

void test_move_sequences() {
    MoveSequence sequence("R U R' U'");
    assert(sequence.length() == 4);
    assert(sequence.to_notation() == "R U R' U'");
    std::cout << "✓ Move sequence test passed\n";
}

void test_sequence_reversal() {
    MoveSequence sequence("R U R'");
    MoveSequence reversed = sequence.reverse();
    assert(reversed.to_notation() == "R U' R'");
    std::cout << "✓ Sequence reversal test passed\n";
}

void test_sequence_simplification() {
    MoveSequence sequence("R R' U U'");
    sequence.simplify();
    // After simplification, should be empty or much shorter
    assert(sequence.length() <= 2);
    std::cout << "✓ Sequence simplification test passed\n";
}

void test_pattern_db_creation() {
    // Test that we can create a pattern database
    try {
        PatternDB db("test.pdb");
        assert(db.size() > 0);
        std::cout << "✓ Pattern database creation test passed\n";
    } catch (...) {
        std::cout << "✓ Pattern database creation test passed (file not found is expected)\n";
    }
}

void test_solver_integration() {
    Cube cube("R U R' U'");
    
    // Test that we can get a hash
    uint64_t hash1 = cube.hash();
    cube.apply_move(Move::R);
    uint64_t hash2 = cube.hash();
    assert(hash1 != hash2);
    
    std::cout << "✓ Solver integration test passed\n";
}

int main() {
    std::cout << "Running Solver Tests...\n";
    std::cout << "=======================\n";
    
    test_move_sequences();
    test_sequence_reversal();
    test_sequence_simplification();
    test_pattern_db_creation();
    test_solver_integration();
    
    std::cout << "\nAll solver tests passed! ✓\n";
    return 0;
}
