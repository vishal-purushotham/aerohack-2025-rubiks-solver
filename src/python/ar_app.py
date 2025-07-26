#!/usr/bin/env python3
"""
AeroHack 2025 AR Cube Solver
Complete integration of AR scanning and Kociemba solving
"""

import sys
import os
import time
from typing import Optional

# Add current directory to Python path
sys.path.append(os.path.dirname(__file__))

# Import our professional components
from kociemba_wrapper import kociemba_solver
from qbr.video import Webcam
from qbr.constants import (
    STICKER_AREA_TILE_SIZE, CUBE_PALETTE,
    E_INCORRECTLY_SCANNED, E_ALREADY_SOLVED
)
from config_manager import config, get_solver_config, get_performance_config, get_colors_config
import simulation_server # Add this import

class AeroHackARSolver:
    """Professional AR + Solver integration for AeroHack 2025."""
    
    def __init__(self):
        """Initialize the professional AR solver system."""
        print("=" * 60)
        print("   AeroHack 2025 Professional Rubik's Cube AR Solver")
        print("   Powered by QBR Computer Vision + Hkociemba Algorithm")
        print("=" * 60)
        print()
        
        # Load configuration
        self.solver_config = get_solver_config()
        self.performance_config = get_performance_config()
        self.colors_config = get_colors_config()
        
        self.solve_count = 0
        self.total_solve_time = self.performance_config.get('initial_solve_time', 0.0)
        self.solutions = []
        
        # Initialize professional QBR webcam scanner
        self.webcam = Webcam()
        print("✓ Professional QBR scanner initialized")
        print("✓ Configuration manager loaded")
    
    def run_ar_interface(self) -> Optional[str]:
        """Run the complete professional AR interface."""
        print("🎯 Starting Professional QBR Cube Scanner...")
        print()
        print("Professional Scanning Instructions:")
        print("1. Hold your scrambled Rubik's cube in front of the camera")
        print("2. Align each face within the detection contours")
        print("3. Use calibration mode (C key) for color accuracy")
        print("4. Press SPACE to capture each face when detected properly")
        print("5. Follow the on-screen face scanning sequence")
        print("6. Professional solver will compute optimal solution!")
        print()
        print("Controls:")
        print("  SPACE - Capture current face")
        print("  C - Toggle calibration mode")
        print("  ESC - Exit scanner")
        print("  R - Reset scanning session")
        print()
        
        try:
            # Start professional QBR scanning with state management
            print("Initializing professional computer vision pipeline...")
            cube_state = self.webcam.run_detection_loop()
            
            if cube_state is None:
                print("❌ Scanning cancelled or failed")
                return None
            
            # Validate the professional cube state
            if not self._validate_cube_state(cube_state):
                print("❌ Invalid cube state detected")
                return None
                
            return cube_state
            
        except Exception as e:
            print(f"❌ Professional scanner error: {e}")
            return None
    
    def _validate_cube_state(self, cube_state: str) -> bool:
        """Validate cube state using professional algorithms."""
        expected_length = self.colors_config.get('total_stickers', 54)
        if not cube_state or len(cube_state) != expected_length:
            print(f"Invalid length: {len(cube_state) if cube_state else 0}, expected 54")
            return False
        
        # Use professional Kociemba validation
        is_valid, message = kociemba_solver.validate_cube_state(cube_state)
        if not is_valid:
            print(f"Validation failed: {message}")
            return False
            
        print(f"✓ Professional validation passed: {message}")
        return True
    
    def solve_cube(self, cube_state: str) -> Optional[str]:
        """Solve cube using professional Hkociemba algorithm."""
        if not cube_state:
            return None
            
        print(f"✓ Cube successfully scanned with professional QBR!")
        print(f"  State: {cube_state[:20]}...")
        print()
        
        # Solve the cube
        print("🧩 Solving cube with professional Hkociemba algorithm...")
        start_time = time.time()
        
        # Get solver configuration
        max_length = self.solver_config.get('max_length', 25)
        timeout = self.solver_config.get('timeout_seconds', 10)
        
        solution = kociemba_solver.solve(cube_state, max_length=max_length, timeout=timeout)
        
        solve_time = time.time() - start_time
        
        if not solution.startswith("Error"):
            print()
            print("🎉 PROFESSIONAL SOLUTION FOUND!")
            print("=" * 40)
            print(f"Solution: {solution}")
            print(f"Solve time: {solve_time:.3f} seconds")
            
            # Parse move count
            if '(' in solution and ')' in solution:
                try:
                    move_info = solution.split('(')[1].split(')')[0]
                    print(f"Move info: {move_info}")
                except:
                    pass
            
            # Update statistics
            self.solve_count += 1
            self.total_solve_time += solve_time
            self.solutions.append(solution)
            
            self.print_statistics()
            
            return solution
        else:
            print(f"❌ Solving failed: {solution}")
            return None
    
    def run_manual_solve(self, cube_string: str) -> Optional[str]:
        """Solve a manually provided cube string."""
        print(f"🧩 Manual solve mode")
        print(f"Cube string: {cube_string}")
        print()
        
        # Validate and solve
        is_valid, message = kociemba_solver.validate_cube_state(cube_string)
        
        if is_valid:
            print(f"✓ {message}")
            
            start_time = time.time()
            
            # Get solver configuration
            max_length = self.solver_config.get('max_length', 25)
            timeout = self.solver_config.get('timeout_seconds', 10)
            
            solution = kociemba_solver.solve(cube_string, max_length=max_length, timeout=timeout)
            solve_time = time.time() - start_time
            
            if not solution.startswith("Error"):
                print()
                print("🎉 SOLUTION FOUND!")
                print("=" * 30)
                print(f"Solution: {solution}")
                print(f"Solve time: {solve_time:.3f} seconds")
                
                self.solve_count += 1
                self.total_solve_time += solve_time
                self.solutions.append(solution)
                
                return solution
            else:
                print(f"❌ Solving failed: {solution}")
        else:
            print(f"❌ Invalid cube: {message}")
        
        return None
    
    def print_statistics(self):
        """Print solving statistics."""
        if self.solve_count > 0:
            avg_time = self.total_solve_time / self.solve_count
            print()
            print("📊 Statistics:")
            print(f"   Total solves: {self.solve_count}")
            print(f"   Average time: {avg_time:.3f} seconds")
            print(f"   Total time: {self.total_solve_time:.3f} seconds")
    
    def run_demo(self):
        """Run a demonstration with known cube states."""
        print("🎮 Demo Mode - Testing with known cube states")
        print()
        
        # Get test cases from configuration
        demo_cubes = config.get('demo_cubes', {})
        test_cases = [
            ("Solved cube", demo_cubes.get('solved', 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB')),
            ("Simple scramble", demo_cubes.get('simple_scramble', 'DRLUUBFBRBLUFRLRLRLLLFFUUFRUBUUBDUUDLDRBDFRFDFFBBUDUL')),
        ]
        
        for name, cube_string in test_cases:
            print(f"Testing: {name}")
            solution = self.run_manual_solve(cube_string)
            print()
            
            if solution:
                print("✓ Test passed")
            else:
                print("❌ Test failed")
            print("-" * 30)
            print()

def main():
    """Main entry point for Professional AR Cube Solver."""
    app = AeroHackARSolver()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--demo":
            app.run_demo()
        elif sys.argv[1] == "--manual" and len(sys.argv) > 2:
            cube_state = sys.argv[2]
            solution = app.run_manual_solve(cube_state)
            if solution:
                # Launch 3D simulation for manual solve
                print("\n🚀 Launching 3D solution animation in your web browser...")
                simulation_server.run_simulation(cube_state, solution)
        else:
            print("Usage:")
            print("  python ar_app.py           # Professional AR scanning mode")
            print("  python ar_app.py --demo    # Demo mode with test cubes")
            print("  python ar_app.py --manual <cube_string>  # Manual solve mode")
    else:
        # Default: Professional AR interface
        print("🚀 Starting Professional AR Interface...")
        cube_state = app.run_ar_interface()
        
        if cube_state:
            print("🎯 Professional cube scanning complete!")
            solution = app.solve_cube(cube_state)
            
            if solution:
                print()
                print("✅ Professional solution generated successfully!")
                print("You can now apply these moves to solve your cube.")
                
                # --- NEW 3D VISUALIZATION LAUNCH ---
                print("\n🚀 Launching 3D solution animation in your web browser...")
                try:
                    # Run the simulation server. This will block until the browser tab is closed.
                    simulation_server.run_simulation(cube_state, solution)
                    print("✅ 3D simulation finished.")
                except Exception as e:
                    print(f"❌ Failed to launch 3D visualization: {e}")
                # ------------------------------------
                    
            else:
                print("❌ Professional solving failed")
        else:
            print("❌ Professional scanning failed or cancelled")

if __name__ == "__main__":
    main()
