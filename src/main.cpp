#include <iostream>
#include <string>
#include "core/cube.hpp"
#include "core/moves.hpp"

using namespace rubiks;

void print_usage() {
    std::cout << "Usage: rubiks_solver [scramble]\n";
    std::cout << "Example: rubiks_solver \"R U R' U'\"\n";
}

int main(int argc, char* argv[]) {
    std::cout << "AeroHack 2025 Rubik's Cube Solver\n";
    std::cout << "==================================\n\n";
    
    // Test basic functionality
    Cube cube;
    std::cout << "Initial cube state: " << cube.to_string() << "\n";
    std::cout << "Is solved: " << (cube.is_solved() ? "Yes" : "No") << "\n\n";
    
    // Apply scramble if provided
    if (argc > 1) {
        std::string scramble = argv[1];
        std::cout << "Applying scramble: " << scramble << "\n";
        
        cube.apply_scramble(scramble);
        std::cout << "After scramble: " << cube.to_string() << "\n";
        std::cout << "Is solved: " << (cube.is_solved() ? "Yes" : "No") << "\n\n";
        
        // Test move sequence
        MoveSequence sequence(scramble);
        std::cout << "Parsed moves: " << sequence.to_notation() << "\n";
        std::cout << "Move count: " << sequence.length() << "\n\n";
        
        // Test reverse sequence
        MoveSequence reverse = sequence.reverse();
        std::cout << "Reverse sequence: " << reverse.to_notation() << "\n";
        
        // Apply reverse to solve
        for (int move : reverse.get_moves()) {
            cube.apply_move(move);
        }
        std::cout << "After applying reverse: " << cube.to_string() << "\n";
        std::cout << "Is solved: " << (cube.is_solved() ? "Yes" : "No") << "\n";
    } else {
        print_usage();
        
        // Demo with a simple sequence
        std::cout << "\nDemo with R U R' U':\n";
        cube.apply_scramble("R U R' U'");
        std::cout << "After R U R' U': " << cube.to_string() << "\n";
        std::cout << "Is solved: " << (cube.is_solved() ? "Yes" : "No") << "\n";
    }
    
    return 0;
}
