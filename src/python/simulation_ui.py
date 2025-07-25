# FILE: src/python/simulation_ui.py
# ACTION: Create this new file.

import vpython as vp
import time
import math

class Cube3DVisualizer:
    """A 3D Rubik's Cube visualizer using VPython."""

    def __init__(self):
        self.scene = vp.canvas(title='AeroHack 2025 - 3D Cube Solver', width=800, height=600)
        self.scene.camera.pos = vp.vector(5, 5, 5)
        self.scene.camera.axis = -vp.vector(5, 5, 5)
        self.cubies = {}
        self.colors = {
            'U': vp.color.white, 'D': vp.color.yellow,
            'R': vp.color.red,   'L': vp.color.orange,
            'F': vp.color.green, 'B': vp.color.blue,
            'GRAY': vp.color.gray(0.3)
        }
        self._build_cube()

    def _build_cube(self):
        """Creates the 26 cubies of the 3x3x3 cube."""
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    if x == 0 and y == 0 and z == 0:
                        continue
                    pos = vp.vector(x, y, z)
                    cubie = vp.box(pos=pos, length=0.98, height=0.98, width=0.98)
                    self.cubies[pos] = cubie
        self._apply_stickers()

    def _apply_stickers(self, state_string=None):
        """Applies colors to the faces of the cubies."""
        # For simplicity, we only color the visible faces of a solved cube.
        # A full implementation would map the state_string to each facelet.
        for pos, cubie in self.cubies.items():
            # Create stickers as thin boxes attached to the cubie
            if pos.y > 0.5: vp.box(pos=cubie.pos + vp.vector(0, 0.5, 0), length=1, height=0.01, width=1, color=self.colors['U'])
            if pos.y < -0.5: vp.box(pos=cubie.pos + vp.vector(0,-0.5, 0), length=1, height=0.01, width=1, color=self.colors['D'])
            if pos.x > 0.5: vp.box(pos=cubie.pos + vp.vector(0.5, 0, 0), length=0.01, height=1, width=1, color=self.colors['R'])
            if pos.x < -0.5: vp.box(pos=cubie.pos + vp.vector(-0.5,0, 0), length=0.01, height=1, width=1, color=self.colors['L'])
            if pos.z > 0.5: vp.box(pos=cubie.pos + vp.vector(0, 0, 0.5), length=1, height=1, width=0.01, color=self.colors['F'])
            if pos.z < -0.5: vp.box(pos=cubie.pos + vp.vector(0, 0,-0.5), length=1, height=1, width=0.01, color=self.colors['B'])
            
    def animate_solution(self, solution_string):
        """Animates a sequence of moves."""
        moves = solution_string.strip().split()
        moves = [m for m in moves if not m.startswith('(')] # Filter out move count

        print(f"Animating {len(moves)} moves...")
        for move in moves:
            self.animate_move(move)
            time.sleep(0.2)

    def animate_move(self, move_str, duration=0.3):
        """Animates a single move."""
        face_map = {
            'U': {'axis': vp.vector(0, 1, 0), 'slice': lambda p: p.y > 0.5, 'angle': -1},
            'D': {'axis': vp.vector(0, 1, 0), 'slice': lambda p: p.y < -0.5, 'angle': 1},
            'R': {'axis': vp.vector(1, 0, 0), 'slice': lambda p: p.x > 0.5, 'angle': -1},
            'L': {'axis': vp.vector(1, 0, 0), 'slice': lambda p: p.x < -0.5, 'angle': 1},
            'F': {'axis': vp.vector(0, 0, 1), 'slice': lambda p: p.z > 0.5, 'angle': -1},
            'B': {'axis': vp.vector(0, 0, 1), 'slice': lambda p: p.z < -0.5, 'angle': 1},
        }

        face = face_map[move_str[0]]
        angle = (math.pi / 2) * face['angle']
        if len(move_str) > 1:
            if move_str[1] == "'": angle *= -1
            if move_str[1] == '2': angle *= 2

        affected_cubies = [c for pos, c in self.cubies.items() if face['slice'](pos)]
        
        steps = 30
        for _ in range(steps):
            vp.rate(int(steps / duration))
            for cubie in affected_cubies:
                cubie.rotate(angle=angle / steps, axis=face['axis'], origin=vp.vector(0,0,0))
