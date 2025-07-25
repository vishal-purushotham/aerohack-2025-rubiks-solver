#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <fstream>
#include "core/cube.hpp"
#include "core/moves.hpp"

using namespace rubiks;

void print_banner() {
    std::cout << "======================================================\n";
    std::cout << "        AeroHack 2025 Rubik's Cube Solver\n";
    std::cout << "   GPU-Accelerated • AI-Guided • AR-Integrated\n";
    std::cout << "======================================================\n\n";
}

void print_usage() {
    std::cout << "Usage:\n";
    std::cout << "  rubiks_solver [options] [scramble]\n\n";
    std::cout << "Options:\n";
    std::cout << "  --ar         Start AR scanning interface\n";
    std::cout << "  --demo       Run demonstration mode\n";
    std::cout << "  --test       Run all tests\n";
    std::cout << "  --python     Launch Python AR interface\n";
    std::cout << "  --help       Show this help message\n\n";
    std::cout << "Examples:\n";
    std::cout << "  rubiks_solver \"R U R' U'\"\n";
    std::cout << "  rubiks_solver --ar\n";
    std::cout << "  rubiks_solver --demo\n";
}

int run_python_interface() {
    std::cout << "🐍 Launching Python AR Interface...\n\n";
    
    // Try to run the Python AR application
    std::string python_cmd = "python ..\\src\\python\\ar_app.py";
    int result = std::system(python_cmd.c_str());
    
    if (result != 0) {
        std::cout << "❌ Failed to launch Python interface.\n";
        std::cout << "Please ensure Python and dependencies are installed:\n";
        std::cout << "  pip install -r requirements.txt\n";
        return 1;
    }
    
    return 0;
}

int run_demo_mode() {
    std::cout << "🎮 Demo Mode - Testing Core Components\n";
    std::cout << "=====================================\n\n";
    
    // Test 1: Basic cube operations
    std::cout << "Test 1: Basic Cube Operations\n";
    std::cout << "------------------------------\n";
    
    Cube cube;
    std::cout << "Initial state: " << cube.to_string() << "\n";
    std::cout << "Is solved: " << (cube.is_solved() ? "Yes" : "No") << "\n";
    
    // Apply some moves
    cube.apply_move(Move::R);
    cube.apply_move(Move::U);
    cube.apply_move(Move::R_PRIME);
    cube.apply_move(Move::U_PRIME);
    
    std::cout << "After R U R' U': " << cube.to_string() << "\n";
    std::cout << "Is solved: " << (cube.is_solved() ? "Yes" : "No") << "\n\n";
    
    // Test 2: Move sequences
    std::cout << "Test 2: Move Sequences\n";
    std::cout << "----------------------\n";
    
    MoveSequence sequence("R U R' U' R U R' U'");
    std::cout << "Sequence: " << sequence.to_notation() << "\n";
    std::cout << "Length: " << sequence.length() << " moves\n";
    
    MoveSequence reversed = sequence.reverse();
    std::cout << "Reversed: " << reversed.to_notation() << "\n\n";
    
    // Test 3: Apply sequence and reverse
    std::cout << "Test 3: Sequence Application\n";
    std::cout << "----------------------------\n";
    
    Cube test_cube;
    for (int move : sequence.get_moves()) {
        test_cube.apply_move(move);
    }
    std::cout << "After sequence: " << test_cube.to_string() << "\n";
    std::cout << "Is solved: " << (test_cube.is_solved() ? "Yes" : "No") << "\n";
    
    // Apply reverse
    for (int move : reversed.get_moves()) {
        test_cube.apply_move(move);
    }
    std::cout << "After reverse: " << test_cube.to_string() << "\n";
    std::cout << "Is solved: " << (test_cube.is_solved() ? "Yes" : "No") << "\n\n";
    
    std::cout << "✅ All demo tests completed!\n\n";
    
    // Suggest next steps
    std::cout << "Next Steps:\n";
    std::cout << "----------\n";
    std::cout << "1. Try AR scanning: rubiks_solver --python\n";
    std::cout << "2. Install Python dependencies: pip install -r requirements.txt\n";
    std::cout << "3. Test with scramble: rubiks_solver \"R U R' U' F R F' U'\"\n";
    
    return 0;
}

int run_tests() {
    std::cout << "🧪 Running Test Suite\n";
    std::cout << "====================\n\n";
    
    // Run the compiled test executables
    std::cout << "Running cube tests...\n";
    int cube_result = std::system("build\\Release\\test_cube.exe");
    
    std::cout << "\nRunning solver tests...\n";
    int solver_result = std::system("build\\Release\\test_solver.exe");
    
    if (cube_result == 0 && solver_result == 0) {
        std::cout << "\n✅ All tests passed!\n";
        return 0;
    } else {
        std::cout << "\n❌ Some tests failed.\n";
        return 1;
    }
}

int main(int argc, char* argv[]) {
    print_banner();
    
    // Parse command line arguments
    if (argc == 1) {
        std::cout << "Welcome to the AeroHack 2025 Rubik's Cube Solver!\n\n";
        print_usage();
        return 0;
    }
    
    std::string arg1 = argv[1];
    
    if (arg1 == "--help" || arg1 == "-h") {
        print_usage();
        return 0;
    }
    else if (arg1 == "--python" || arg1 == "--ar") {
        return run_python_interface();
    }
    else if (arg1 == "--demo") {
        return run_demo_mode();
    }
    else if (arg1 == "--test") {
        return run_tests();
    }
    else {
        // Treat as scramble
        std::string scramble = arg1;
        
        std::cout << "🧩 Solving Cube with C++ Engine\n";
        std::cout << "===============================\n";
        std::cout << "Scramble: " << scramble << "\n\n";
        
        // Test basic functionality
        Cube cube;
        std::cout << "Initial state: " << cube.to_string() << "\n";
        std::cout << "Is solved: " << (cube.is_solved() ? "Yes" : "No") << "\n\n";
        
        // Apply scramble
        cube.apply_scramble(scramble);
        std::cout << "After scramble: " << cube.to_string() << "\n";
        std::cout << "Is solved: " << (cube.is_solved() ? "Yes" : "No") << "\n\n";
        
        // Parse and test moves
        MoveSequence sequence(scramble);
        std::cout << "Parsed moves: " << sequence.to_notation() << "\n";
        std::cout << "Move count: " << sequence.length() << "\n\n";
        
        // Generate reverse sequence (simple unscramble)
        MoveSequence reverse = sequence.reverse();
        std::cout << "Reverse sequence: " << reverse.to_notation() << "\n";
        
        // Apply reverse to solve
        for (int move : reverse.get_moves()) {
            cube.apply_move(move);
        }
        std::cout << "After applying reverse: " << cube.to_string() << "\n";
        std::cout << "Is solved: " << (cube.is_solved() ? "Yes" : "No") << "\n\n";
        
        std::cout << "💡 For advanced solving with Kociemba algorithm:\n";
        std::cout << "   Run: rubiks_solver --python\n";
    }
    
    return 0;
}
