#include <cassert>
#include <iostream>
#include "../src/core/cube.hpp"

using namespace rubiks;

void test_cube_initialization() {
    Cube cube;
    assert(cube.is_solved());
    std::cout << "✓ Cube initialization test passed\n";
}

void test_move_application() {
    Cube cube;
    cube.apply_move(R1);
    assert(!cube.is_solved());
    
    // Apply R' to undo
    cube.apply_move(R3);
    assert(cube.is_solved());
    std::cout << "✓ Move application test passed\n";
}

void test_scramble_parsing() {
    Cube cube("R U R' U'");
    assert(!cube.is_solved());
    std::cout << "✓ Scramble parsing test passed\n"; 
}

void test_state_operations() {
    Cube cube1;
    Cube cube2;
    
    // Test hash function
    assert(cube1.hash() == cube2.hash());
    
    cube1.apply_move(R1);
    assert(cube1.hash() != cube2.hash());
    
    std::cout << "✓ State operations test passed\n";
}

int main() {
    std::cout << "Running Cube Tests...\n";
    std::cout << "=====================\n";
    
    test_cube_initialization();
    test_move_application();
    test_scramble_parsing();
    test_state_operations();
    
    std::cout << "\nAll cube tests passed! ✓\n";
    return 0;
}
