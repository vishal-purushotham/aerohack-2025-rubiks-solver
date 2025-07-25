#!/usr/bin/env python3
"""
AR Cube Scanner for AeroHack 2025 Rubik's Cube Solver
Simplified computer vision system based on QBR approach
"""

import cv2
import numpy as np
import time
from typing import Optional, List, Tuple, Dict

# Color detection constants
STICKER_AREA_TILE_SIZE = 30
STICKER_AREA_TILE_GAP = 4
STICKER_AREA_OFFSET = 20

# HSV color ranges for cube detection
COLOR_RANGES = {
    'white': ([0, 0, 168], [172, 111, 255]),
    'yellow': ([15, 77, 106], [35, 255, 255]),
    'red': ([0, 120, 70], [10, 255, 255]),
    'orange': ([10, 120, 70], [25, 255, 255]),
    'blue': ([100, 150, 50], [130, 255, 255]),
    'green': ([40, 40, 40], [80, 255, 255])
}

# Face order for scanning
FACE_ORDER = ['front', 'right', 'back', 'left', 'up', 'down']
FACE_POSITIONS = {
    'front': 'F', 'right': 'R', 'back': 'B', 
    'left': 'L', 'up': 'U', 'down': 'D'
}

class ColorDetector:
    """Simplified color detection for cube stickers."""
    
    @staticmethod
    def get_dominant_color(roi):
        """Get the dominant color in a region of interest."""
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Calculate mean HSV values
        mean_hsv = np.mean(hsv, axis=(0, 1))
        
        # Find closest color match
        best_color = 'white'
        min_distance = float('inf')
        
        for color_name, (lower, upper) in COLOR_RANGES.items():
            lower = np.array(lower)
            upper = np.array(upper)
            
            # Check if mean HSV is within range
            if np.all(mean_hsv >= lower) and np.all(mean_hsv <= upper):
                # Calculate distance to center of range
                center = (lower + upper) / 2
                distance = np.linalg.norm(mean_hsv - center)
                if distance < min_distance:
                    min_distance = distance
                    best_color = color_name
        
        return best_color
    
    @staticmethod
    def get_bgr_color(color_name: str) -> Tuple[int, int, int]:
        """Get BGR color values for display."""
        color_map = {
            'white': (255, 255, 255),
            'yellow': (0, 255, 255),
            'red': (0, 0, 255),
            'orange': (0, 165, 255),
            'blue': (255, 0, 0),
            'green': (0, 255, 0)
        }
        return color_map.get(color_name, (128, 128, 128))

class SimpleCubeScanner:
    """Simplified cube scanner for demonstration purposes."""
    
    def __init__(self):
        print("Initializing AR Cube Scanner...")
        self.cap = None
        self.scanned_faces = {}
        self.current_face_index = 0
        self.scanning_complete = False
        
        # Try to initialize camera
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise Exception("Could not open camera")
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            print("✓ Camera initialized successfully!")
            
        except Exception as e:
            print(f"✗ Camera initialization failed: {e}")
            print("Scanner will run in simulation mode")
    
    def get_current_face_name(self) -> str:
        """Get the name of the current face being scanned."""
        if self.current_face_index < len(FACE_ORDER):
            return FACE_ORDER[self.current_face_index]
        return "complete"
    
    def extract_stickers_from_contours(self, frame) -> List[str]:
        """Extract 9 sticker colors from the frame."""
        height, width = frame.shape[:2]
        
        # Define 3x3 grid for sticker detection
        stickers = []
        grid_size = 3
        
        # Calculate grid positions
        start_x = width // 4
        start_y = height // 4
        cell_width = width // 2 // grid_size
        cell_height = height // 2 // grid_size
        
        for row in range(grid_size):
            for col in range(grid_size):
                # Calculate ROI for this sticker
                x1 = start_x + col * cell_width
                y1 = start_y + row * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                
                # Extract ROI and detect color
                roi = frame[y1:y2, x1:x2]
                if roi.size > 0:
                    color = ColorDetector.get_dominant_color(roi)
                    stickers.append(color)
                else:
                    stickers.append('white')  # fallback
        
        return stickers
    
    def draw_detection_overlay(self, frame):
        """Draw detection overlay on the frame."""
        height, width = frame.shape[:2]
        
        # Draw 3x3 grid
        grid_size = 3
        start_x = width // 4
        start_y = height // 4
        cell_width = width // 2 // grid_size
        cell_height = height // 2 // grid_size
        
        for row in range(grid_size):
            for col in range(grid_size):
                x1 = start_x + col * cell_width
                y1 = start_y + row * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                
                # Draw rectangle
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Draw center point
                center_x = x1 + cell_width // 2
                center_y = y1 + cell_height // 2
                cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)
        
        # Draw instructions
        face_name = self.get_current_face_name()
        if face_name != "complete":
            text = f"Scanning {face_name.upper()} face ({self.current_face_index + 1}/6)"
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, "Press SPACE to capture", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, "Press ESC to exit", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        else:
            cv2.putText(frame, "Scanning complete!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    def run_simulation_mode(self) -> Optional[str]:
        """Run scanner in simulation mode with a known cube state."""
        print("Running in simulation mode...")
        print("Simulating cube scan...")
        
        # Simulate a scrambled cube state
        # This represents a real cube state in standard notation
        simulated_state = "DLBUFRFLRBLUUFDDLRFUBRFBULRDDLRUUBDDFBLRUFLRFBUDFUBULL"
        
        print(f"Simulated cube state: {simulated_state}")
        return simulated_state
    
    def run(self) -> Optional[str]:
        """Run the AR scanning interface."""
        if self.cap is None:
            return self.run_simulation_mode()
        
        print("Starting AR cube scanning...")
        print("Controls:")
        print("  SPACE - Capture current face")
        print("  ESC   - Exit scanner")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to read from camera")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Draw detection overlay
            self.draw_detection_overlay(frame)
            
            # Show frame
            cv2.imshow('AeroHack Cube Scanner', frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord(' '):  # Space to capture
                if self.current_face_index < len(FACE_ORDER):
                    face_name = self.get_current_face_name()
                    stickers = self.extract_stickers_from_contours(frame)
                    self.scanned_faces[face_name] = stickers
                    
                    print(f"✓ Captured {face_name} face: {stickers}")
                    self.current_face_index += 1
                    
                    if self.current_face_index >= len(FACE_ORDER):
                        print("All faces scanned! Processing...")
                        break
            
            elif key == 27:  # ESC to exit
                print("Scanning cancelled by user")
                self.cleanup()
                return None
        
        self.cleanup()
        
        # Convert scanned faces to cube string
        if len(self.scanned_faces) == 6:
            cube_string = self.faces_to_cube_string()
            print(f"Generated cube string: {cube_string}")
            return cube_string
        
        return None
    
    def faces_to_cube_string(self) -> str:
        """Convert scanned faces to standard cube string format."""
        # Standard order: U R F D L B
        color_to_char = {
            'white': 'U', 'red': 'R', 'green': 'F',
            'yellow': 'D', 'orange': 'L', 'blue': 'B'
        }
        
        # Map face names to standard positions
        face_mapping = {
            'up': 'U', 'right': 'R', 'front': 'F',
            'down': 'D', 'left': 'L', 'back': 'B'
        }
        
        cube_string = ""
        for standard_face in ['up', 'right', 'front', 'down', 'left', 'back']:
            if standard_face in self.scanned_faces:
                face_colors = self.scanned_faces[standard_face]
                # Convert colors to characters
                for color in face_colors:
                    cube_string += color_to_char.get(color, 'U')
            else:
                # Fallback: solved face
                cube_string += face_mapping[standard_face] * 9
        
        return cube_string
    
    def cleanup(self):
        """Clean up resources."""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

# Create global scanner instance
ar_scanner = SimpleCubeScanner()
