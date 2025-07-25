# Professional Hkociemba Two-Phase Solver
"""
Herbert Kociemba's Two-Phase Algorithm for solving Rubik's Cube.
This is the professional implementation from https://github.com/hkociemba/RubiksCube-TwophaseSolver

The solver uses sophisticated algorithms:
- Phase 1: Solve edge orientation, corner orientation, and E-slice position
- Phase 2: Solve the remaining cube with restricted moves
- Symmetry reduction and pruning tables for optimal performance
- Multi-threading for faster solutions
"""

from .solver import solve, solveto
from .face import FaceCube
from .cubie import CubieCube

__all__ = ['solve', 'solveto', 'FaceCube', 'CubieCube']
