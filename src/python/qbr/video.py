#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: fenc=utf-8 ts=4 sw=4 et

import cv2
import os
import sys
from .colordetection import color_detector
from .config import config
from .helpers import get_next_locale

# Add parent directory to path for main config import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config_manager import get_camera_config

from PIL import ImageFont, ImageDraw, Image
import numpy as np
from .constants import (
    COLOR_PLACEHOLDER,
    LOCALES,
    ROOT_DIR,
    CUBE_PALETTE,
    MINI_STICKER_AREA_TILE_SIZE,
    MINI_STICKER_AREA_TILE_GAP,
    MINI_STICKER_AREA_OFFSET,
    STICKER_AREA_TILE_SIZE,
    STICKER_AREA_TILE_GAP,
    STICKER_AREA_OFFSET,
    STICKER_CONTOUR_COLOR,
    CALIBRATE_MODE_KEY,
    SWITCH_LANGUAGE_KEY,
    TEXT_SIZE,
    E_INCORRECTLY_SCANNED,
    E_ALREADY_SOLVED
)

class Webcam:

    def __init__(self):
        print('Starting webcam... (this might take a while, please be patient)')
        
        # Initialize camera configuration
        self.camera_config = get_camera_config()
        self.detection_config = self.camera_config.get('detection', {})
        self.calibration_config = self.camera_config.get('calibration', {})
        self.ui_config = self.camera_config.get('ui', {})
        self.controls_config = self.camera_config.get('controls', {})
        
        # Get camera index from config
        camera_index = self.camera_config.get('camera_index', 0)
        self.cam = cv2.VideoCapture(camera_index)
        print('Webcam successfully started')

        self.colors_to_calibrate = ['green', 'red', 'blue', 'orange', 'white', 'yellow']
        self.average_sticker_colors = {}
        self.result_state = {}

        # Initialize with default color from config
        default_color = tuple(self.camera_config.get('default_color', [255, 255, 255]))
        self.snapshot_state = [default_color] * 9
        self.preview_state = [default_color] * 9

        # Set resolution from config
        resolution = self.camera_config.get('resolution', {'width': 640, 'height': 480})
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, resolution['width'])
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution['height'])
        self.width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.calibrate_mode = False
        self.calibrated_colors = {}
        self.current_color_to_calibrate_index = 0
        self.done_calibrating = False

        # Manual color correction mode
        self.manual_correction_mode = False
        self.available_colors = ['white', 'red', 'green', 'yellow', 'orange', 'blue']
        self.color_bgr_values = {
            'white': (255, 255, 255),
            'red': (0, 0, 255),
            'green': (0, 255, 0),
            'yellow': (0, 255, 255),
            'orange': (0, 165, 255),
            'blue': (255, 0, 0)
        }
        
        # For manual correction, we need to track which colors correspond to which notation
        self.color_to_notation = {
            'white': 'U',
            'red': 'R',
            'green': 'F',
            'yellow': 'D',
            'orange': 'L',
            'blue': 'B'
        }

    def mouse_callback(self, event, x, y, flags, param):
        """Handle mouse clicks for manual color correction."""
        if event == cv2.EVENT_LBUTTONDOWN and self.manual_correction_mode:
            # Check if click is in preview area
            preview_x = STICKER_AREA_OFFSET
            preview_y = STICKER_AREA_OFFSET
            preview_width = STICKER_AREA_TILE_SIZE * 3 + STICKER_AREA_TILE_GAP * 2
            preview_height = STICKER_AREA_TILE_SIZE * 3 + STICKER_AREA_TILE_GAP * 2
            
            if (preview_x <= x <= preview_x + preview_width and 
                preview_y <= y <= preview_y + preview_height):
                
                # Calculate which tile was clicked
                rel_x = x - preview_x
                rel_y = y - preview_y
                
                # Account for gaps between tiles
                col = min(2, rel_x // (STICKER_AREA_TILE_SIZE + STICKER_AREA_TILE_GAP))
                row = min(2, rel_y // (STICKER_AREA_TILE_SIZE + STICKER_AREA_TILE_GAP))
                
                # Make sure click is actually on a tile, not in the gap
                tile_start_x = col * (STICKER_AREA_TILE_SIZE + STICKER_AREA_TILE_GAP)
                tile_start_y = row * (STICKER_AREA_TILE_SIZE + STICKER_AREA_TILE_GAP)
                
                if (tile_start_x <= rel_x <= tile_start_x + STICKER_AREA_TILE_SIZE and
                    tile_start_y <= rel_y <= tile_start_y + STICKER_AREA_TILE_SIZE):
                    
                    sticker_index = row * 3 + col
                    self.cycle_sticker_color(sticker_index)

    def cycle_sticker_color(self, sticker_index):
        """Cycle through available colors for a specific sticker."""
        if 0 <= sticker_index < 9:
            # Get current color of this sticker
            current_bgr = self.preview_state[sticker_index]
            
            # Handle case where current_bgr might be a string (from previous errors)
            if isinstance(current_bgr, str):
                # Convert string back to a proper BGR value
                current_bgr = (255, 255, 255)  # Default to white
            elif not isinstance(current_bgr, (tuple, list)) or len(current_bgr) != 3:
                # Handle invalid BGR values
                current_bgr = (255, 255, 255)  # Default to white
            
            # Find current color in our palette
            current_color_name = None
            for color_name, bgr_value in self.color_bgr_values.items():
                if tuple(current_bgr) == tuple(bgr_value):
                    current_color_name = color_name
                    break
            
            # Get next color in cycle
            if current_color_name in self.available_colors:
                current_index = self.available_colors.index(current_color_name)
                next_index = (current_index + 1) % len(self.available_colors)
            else:
                # If current color not found, start from white
                next_index = 0
            
            next_color_name = self.available_colors[next_index]
            # IMPORTANT: Store BGR tuple, not string!
            self.preview_state[sticker_index] = self.color_bgr_values[next_color_name]
            print(f"Tile {sticker_index} changed to {next_color_name}")

    def draw_stickers(self, stickers, offset_x, offset_y):
        """Draws the given stickers onto the given frame."""
        index = -1
        for row in range(3):
            for col in range(3):
                index += 1
                x1 = (offset_x + STICKER_AREA_TILE_SIZE * col) + STICKER_AREA_TILE_GAP * col
                y1 = (offset_y + STICKER_AREA_TILE_SIZE * row) + STICKER_AREA_TILE_GAP * row
                x2 = x1 + STICKER_AREA_TILE_SIZE
                y2 = y1 + STICKER_AREA_TILE_SIZE

                # shadow
                cv2.rectangle(
                    self.frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 0, 0),
                    -1
                )

                # foreground color
                cv2.rectangle(
                    self.frame,
                    (x1 + 1, y1 + 1),
                    (x2 - 1, y2 - 1),
                    color_detector.get_prominent_color(stickers[index]),
                    -1
                )

    def draw_preview_stickers(self):
        """Draw the current preview state onto the given frame."""
        self.draw_stickers(self.preview_state, STICKER_AREA_OFFSET, STICKER_AREA_OFFSET)

    def draw_snapshot_stickers(self):
        """Draw the current snapshot state onto the given frame."""
        y = STICKER_AREA_TILE_SIZE * 3 + STICKER_AREA_TILE_GAP * 2 + STICKER_AREA_OFFSET * 2
        self.draw_stickers(self.snapshot_state, STICKER_AREA_OFFSET, y)

    def find_contours(self, dilatedFrame):
        """Find the contours of a 3x3x3 cube."""
        contours, hierarchy = cv2.findContours(dilatedFrame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        final_contours = []

        # Step 1/4: filter all contours to only those that are square-ish shapes.
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.1 * perimeter, True)
            if len (approx) == 4:
                area = cv2.contourArea(contour)
                (x, y, w, h) = cv2.boundingRect(approx)

                # Find aspect ratio of boundary rectangle around the countours.
                ratio = w / float(h)

                # Check if contour is close to a square using configuration values.
                min_ratio = self.detection_config.get('min_aspect_ratio', 0.8)
                max_ratio = self.detection_config.get('max_aspect_ratio', 1.2)
                min_width = self.detection_config.get('min_sticker_width', 30)
                max_width = self.detection_config.get('max_sticker_width', 60)
                min_area_ratio = self.detection_config.get('min_area_ratio', 0.4)
                
                if (ratio >= min_ratio and ratio <= max_ratio and 
                    w >= min_width and w <= max_width and 
                    area / (w * h) > min_area_ratio):
                    final_contours.append((x, y, w, h))

        # Return early if we didn't found 9 or more contours.
        expected_contours = self.calibration_config.get('expected_neighbors', 9)
        if len(final_contours) < expected_contours:
            return []

        # Step 2/4: Find the contour that has 9 neighbors (including itself)
        # and return all of those neighbors.
        found = False
        contour_neighbors = {}
        for index, contour in enumerate(final_contours):
            (x, y, w, h) = contour
            contour_neighbors[index] = []
            center_x = x + w / 2
            center_y = y + h / 2
            radius = self.calibration_config.get('neighbor_search_radius', 1.5)

            # Create 9 positions for the current contour which are the
            # neighbors. We'll use this to check how many neighbors each contour
            # has. The only way all of these can match is if the current contour
            # is the center of the cube. If we found the center, we also know
            # all the neighbors, thus knowing all the contours and thus knowing
            # this shape can be considered a 3x3x3 cube. When we've found those
            # contours, we sort them and return them.
            neighbor_positions = [
                # top left
                [(center_x - w * radius), (center_y - h * radius)],

                # top middle
                [center_x, (center_y - h * radius)],

                # top right
                [(center_x + w * radius), (center_y - h * radius)],

                # middle left
                [(center_x - w * radius), center_y],

                # center
                [center_x, center_y],

                # middle right
                [(center_x + w * radius), center_y],

                # bottom left
                [(center_x - w * radius), (center_y + h * radius)],

                # bottom middle
                [center_x, (center_y + h * radius)],

                # bottom right
                [(center_x + w * radius), (center_y + h * radius)],
            ]

            for neighbor in final_contours:
                (x2, y2, w2, h2) = neighbor
                for (x3, y3) in neighbor_positions:
                    # The neighbor_positions are located in the center of each
                    # contour instead of top-left corner.
                    # logic: (top left < center pos) and (bottom right > center pos)
                    if (x2 < x3 and y2 < y3) and (x2 + w2 > x3 and y2 + h2 > y3):
                        contour_neighbors[index].append(neighbor)

        # Step 3/4: Now that we know how many neighbors all contours have, we'll
        # loop over them and find the contour that has 9 neighbors, which
        # includes itself. This is the center piece of the cube. If we come
        # across it, then the 'neighbors' are actually all the contours we're
        # looking for.
        for (contour, neighbors) in contour_neighbors.items():
            expected_neighbors = self.calibration_config.get('expected_neighbors', 9)
            if len(neighbors) == expected_neighbors:
                found = True
                final_contours = neighbors
                break

        if not found:
            return []

        # Step 4/4: When we reached this part of the code we found a cube-like
        # contour. The code below will sort all the contours on their X and Y
        # values from the top-left to the bottom-right.

        # Sort contours on the y-value first.
        y_sorted = sorted(final_contours, key=lambda item: item[1])

        # Split into 3 rows and sort each row on the x-value.
        top_row = sorted(y_sorted[0:3], key=lambda item: item[0])
        middle_row = sorted(y_sorted[3:6], key=lambda item: item[0])
        bottom_row = sorted(y_sorted[6:9], key=lambda item: item[0])

        sorted_contours = top_row + middle_row + bottom_row
        return sorted_contours

    def scanned_successfully(self):
        """Validate if the user scanned 9 colors for each side."""
        color_count = {}
        for side, preview in self.result_state.items():
            for bgr in preview:
                key = str(bgr)
                if key not in color_count:
                    color_count[key] = 1
                else:
                    color_count[key] = color_count[key] + 1
        stickers_per_color = self.calibration_config.get('expected_stickers_per_color', 9)
        invalid_colors = [k for k, v in color_count.items() if v != stickers_per_color]
        return len(invalid_colors) == 0

    def draw_contours(self, contours):
        """Draw contours onto the given frame."""
        if self.calibrate_mode:
            # Only show the center piece contour.
            (x, y, w, h) = contours[4]
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), STICKER_CONTOUR_COLOR, 2)
        else:
            for index, (x, y, w, h) in enumerate(contours):
                cv2.rectangle(self.frame, (x, y), (x + w, y + h), STICKER_CONTOUR_COLOR, 2)

    def update_preview_state(self, contours):
        """
        Get the average color value for the contour for every X amount of frames
        to prevent flickering and more precise results.
        """
        max_average_rounds = 8
        for index, (x, y, w, h) in enumerate(contours):
            if index in self.average_sticker_colors and len(self.average_sticker_colors[index]) == max_average_rounds:
                sorted_items = {}
                for bgr in self.average_sticker_colors[index]:
                    key = str(bgr)
                    if key in sorted_items:
                        sorted_items[key] += 1
                    else:
                        sorted_items[key] = 1
                most_common_color = max(sorted_items, key=lambda i: sorted_items[i])
                self.average_sticker_colors[index] = []
                self.preview_state[index] = eval(most_common_color)
                break

            roi = self.frame[y+7:y+h-7, x+14:x+w-14]
            avg_bgr = color_detector.get_dominant_color(roi)
            closest_color = color_detector.get_closest_color(avg_bgr)['color_bgr']
            self.preview_state[index] = closest_color
            if index in self.average_sticker_colors:
                self.average_sticker_colors[index].append(closest_color)
            else:
                self.average_sticker_colors[index] = [closest_color]

    def update_snapshot_state(self):
        """Update the snapshot state based on the current preview state."""
        self.snapshot_state = list(self.preview_state)
        
        # Ensure all elements in snapshot_state are proper BGR tuples
        for i in range(len(self.snapshot_state)):
            if isinstance(self.snapshot_state[i], str):
                # Convert string back to BGR tuple (this shouldn't happen with fixed manual mode)
                self.snapshot_state[i] = (255, 255, 255)  # Default to white
            elif not isinstance(self.snapshot_state[i], (tuple, list)) or len(self.snapshot_state[i]) != 3:
                self.snapshot_state[i] = (255, 255, 255)  # Default to white
        
        try:
            center_color_info = color_detector.get_closest_color(self.snapshot_state[4])
            if isinstance(center_color_info, dict) and 'color_name' in center_color_info:
                center_color_name = center_color_info['color_name']
            else:
                print(f"Warning: Invalid color detection result for center sticker: {center_color_info}")
                center_color_name = 'white'  # Default fallback
        except Exception as e:
            print(f"Error detecting center color: {e}")
            center_color_name = 'white'  # Default fallback
            
        self.result_state[center_color_name] = self.snapshot_state
        self.draw_snapshot_stickers()

    def get_font(self, size=TEXT_SIZE):
        """Load the truetype font with the specified text size."""
        try:
            font_path = f'{ROOT_DIR}/assets/arial-unicode-ms.ttf'
            return ImageFont.truetype(font_path, size)
        except:
            # Fallback to default font if custom font not available
            return ImageFont.load_default()

    def render_text(self, text, pos, color=(255, 255, 255), size=TEXT_SIZE, anchor='lt'):
        """
        Render text with a shadow using the pillow module.
        """
        font = self.get_font(size)

        # Convert opencv frame (np.array) to PIL Image array.
        frame = Image.fromarray(self.frame)

        # Draw the text onto the image.
        draw = ImageDraw.Draw(frame)
        try:
            draw.text(pos, text, font=font, fill=color, anchor=anchor,
                      stroke_width=1, stroke_fill=(0, 0, 0))
        except:
            # Fallback for older PIL versions
            draw.text(pos, text, font=font, fill=color)

        # Convert the pillow frame back to a numpy array.
        self.frame = np.array(frame)

    def get_text_size(self, text, size=TEXT_SIZE):
        """Get text size based on the default freetype2 loaded font."""
        try:
            return self.get_font(size).getsize(text)
        except:
            # Fallback for newer PIL versions
            bbox = self.get_font(size).getbbox(text)
            return (bbox[2] - bbox[0], bbox[3] - bbox[1])

    def draw_scanned_sides(self):
        """Display how many sides are scanned by the user."""
        text = f'Scanned sides: {len(self.result_state.keys())}/6'
        self.render_text(text, (20, self.height - 20), anchor='lb')

    def draw_current_color_to_calibrate(self):
        """Display the current side's color that needs to be calibrated."""
        offset_y = self.ui_config.get('text_offset_y', 20)
        font_size = int(TEXT_SIZE * 1.25)
        if self.done_calibrating:
            messages = [
                'Calibrated successfully',
                f'Press {CALIBRATE_MODE_KEY} to quit calibrate mode',
            ]
            for index, text in enumerate(messages):
                _, textsize_height = self.get_text_size(text, font_size)
                y = offset_y + (textsize_height + 10) * index
                self.render_text(text, (int(self.width / 2), y), size=font_size, anchor='mt')
        else:
            current_color = self.colors_to_calibrate[self.current_color_to_calibrate_index]
            messages = [
                f'Calibrate the {current_color} side',
                'Position center sticker in detection area and press SPACE',
                f'Or use shortcut: Ctrl+{current_color[0].upper()} to force {current_color}',
                'Shortcuts: Ctrl+W(white) Ctrl+R(red) Ctrl+G(green)',
                'Ctrl+Y(yellow) Ctrl+O(orange) Ctrl+B(blue)'
            ]
            
            for index, text in enumerate(messages):
                _, textsize_height = self.get_text_size(text, 14 if index > 0 else font_size)
                y = offset_y + (textsize_height + 5) * index
                color = (255, 255, 255) if index <= 1 else (0, 255, 255)  # Yellow for shortcuts
                size = font_size if index <= 1 else 14
                self.render_text(text, (int(self.width / 2), y), color=color, size=size, anchor='mt')

    def draw_calibrated_colors(self):
        """Display all the colors that are calibrated while in calibrate mode."""
        offset_y = self.ui_config.get('text_offset_y', 20)
        for index, (color_name, color_bgr) in enumerate(self.calibrated_colors.items()):
            x1 = self.ui_config.get('color_grid_x1', 90)
            y1 = int(offset_y + STICKER_AREA_TILE_SIZE * index)
            x2 = x1 + STICKER_AREA_TILE_SIZE
            y2 = y1 + STICKER_AREA_TILE_SIZE

            # shadow
            cv2.rectangle(
                self.frame,
                (x1, y1),
                (x2, y2),
                (0, 0, 0),
                -1
            )

            # foreground
            cv2.rectangle(
                self.frame,
                (x1 + 1, y1 + 1),
                (x2 - 1, y2 - 1),
                tuple([int(c) for c in color_bgr]),
                -1
            )
            self.render_text(color_name, (20, y1 + STICKER_AREA_TILE_SIZE / 2 - 3), anchor='lm')

    def reset_calibrate_mode(self):
        """Reset calibrate mode variables."""
        self.calibrated_colors = {}
        self.current_color_to_calibrate_index = 0
        self.done_calibrating = False

    def force_calibrate_color(self, color_name):
        """Force calibrate the current color with a predefined BGR value."""
        if color_name in self.colors_to_calibrate:
            # Use predefined BGR values for forced calibration
            predefined_bgr = {
                'white': (255, 255, 255),
                'red': (0, 0, 255),
                'green': (0, 255, 0),
                'yellow': (0, 255, 255),
                'orange': (0, 165, 255),
                'blue': (255, 0, 0)
            }
            
            current_color = self.colors_to_calibrate[self.current_color_to_calibrate_index]
            if current_color == color_name:
                # Force the calibration with predefined color
                self.calibrated_colors[current_color] = predefined_bgr[color_name]
                self.current_color_to_calibrate_index += 1
                self.done_calibrating = self.current_color_to_calibrate_index == len(self.colors_to_calibrate)
                
                print(f"✓ Forced calibration: {color_name} = {predefined_bgr[color_name]}")
                
                if self.done_calibrating:
                    color_detector.set_cube_color_pallete(self.calibrated_colors)
                    config.set_setting(CUBE_PALETTE, color_detector.cube_color_palette)
                    print("✓ Calibration complete!")
            else:
                print(f"Warning: Currently calibrating {current_color}, not {color_name}")
        else:
            print(f"Error: {color_name} is not a valid color for calibration")

    def draw_manual_correction_instructions(self):
        """Draw instructions for manual color correction mode."""
        if self.manual_correction_mode:
            y_start = 50
            instructions = [
                "MANUAL CORRECTION MODE",
                "Click on any tile in preview to cycle colors",
                "Available: White → Red → Green → Yellow → Orange → Blue",
                "Press M to exit manual mode"
            ]
            
            for i, instruction in enumerate(instructions):
                color = (0, 255, 255) if i == 0 else (255, 255, 255)  # Yellow for title, white for others
                size = 20 if i == 0 else 16
                self.render_text(instruction, (20, y_start + i * 25), color=color, size=size)

    def draw_current_language(self):
        """Draw the current language."""
        margin = self.ui_config.get('margin', 20)
        text = config.get_setting('locale', 'en').upper() + ' | ' + LOCALES[config.get_setting('locale', 'en')]
        self.render_text(text, (margin, self.height - margin), size=16, anchor='lb')
        text = f'Language: {LOCALES[config.get_setting("locale", "en")]}'
        offset = 20
        self.render_text(text, (self.width - offset, offset), anchor='rt')

    def draw_2d_cube_state(self):
        """
        Create a 2D cube state visualization and draw the self.result_state.

        We're gonna display the visualization like so:
                    -----
                  | W W W |
                  | W W W |
                  | W W W |
            -----   -----   -----   -----
          | O O O | G G G | R R R | B B B |
          | O O O | G G G | R R R | B B B |
          | O O O | G G G | R R R | B B B |
            -----   -----   -----   -----
                  | Y Y Y |
                  | Y Y Y |
                  | Y Y Y |
                    -----
        So we're gonna make a 4x3 grid and hardcode where each side has to go.
        Based on the x and y in that 4x3 grid we can calculate its position.
        """
        grid = {
            'white' : [1, 0],
            'orange': [0, 1],
            'green' : [1, 1],
            'red'   : [2, 1],
            'blue'  : [3, 1],
            'yellow': [1, 2],
        }

        # The offset in-between each side (white, red, etc).
        side_offset = MINI_STICKER_AREA_TILE_GAP * 3

        # The size of 1 whole side (containing 9 stickers).
        side_size = MINI_STICKER_AREA_TILE_SIZE * 3 + MINI_STICKER_AREA_TILE_GAP * 2

        # The X and Y offset is placed in the bottom-right corner, minus the
        # whole size of the 4x3 grid, minus an additional offset.
        offset_x = self.width - (side_size * 4) - (side_offset * 3) - MINI_STICKER_AREA_OFFSET
        offset_y = self.height - (side_size * 3) - (side_offset * 2) - MINI_STICKER_AREA_OFFSET

        for side, (grid_x, grid_y) in grid.items():
            index = -1
            for row in range(3):
                for col in range(3):
                    index += 1
                    x1 = int(
                        (offset_x + MINI_STICKER_AREA_TILE_SIZE * col) +
                        (MINI_STICKER_AREA_TILE_GAP * col) +
                        ((side_size + side_offset) * grid_x)
                    )
                    y1 = int(
                        (offset_y + MINI_STICKER_AREA_TILE_SIZE * row) +
                        (MINI_STICKER_AREA_TILE_GAP * row) +
                        ((side_size + side_offset) * grid_y)
                    )
                    x2 = int(x1 + MINI_STICKER_AREA_TILE_SIZE)
                    y2 = int(y1 + MINI_STICKER_AREA_TILE_SIZE)

                    foreground_color = COLOR_PLACEHOLDER
                    if side in self.result_state:
                        foreground_color = color_detector.get_prominent_color(self.result_state[side][index])

                    # shadow
                    cv2.rectangle(
                        self.frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 0, 0),
                        -1
                    )

                    # foreground color
                    cv2.rectangle(
                        self.frame,
                        (x1 + 1, y1 + 1),
                        (x2 - 1, y2 - 1),
                        foreground_color,
                        -1
                    )

    def get_result_notation(self):
        """
        Convert all the sides and their BGR colors to the standard Kociemba notation string.
        The order MUST BE URFDLB (Up, Right, Front, Down, Left, Back).
        - Up: White
        - Right: Red
        - Front: Green
        - Down: Yellow
        - Left: Orange
        - Back: Blue
        """
        try:
            notation = dict(self.result_state)
            for side, preview in notation.items():
                for sticker_index, bgr in enumerate(preview):
                    try:
                        notation[side][sticker_index] = color_detector.convert_bgr_to_notation(bgr)
                    except (KeyError, IndexError, TypeError) as e:
                        print(f"Warning: Could not convert color {bgr} for side {side}, sticker {sticker_index}: {e}")
                        # Use a fallback notation
                        notation[side][sticker_index] = 'U'  # Default to white/up

            # Standard Kociemba face order: U, R, F, D, L, B
            # This corresponds to our color mapping: white, red, green, yellow, orange, blue
            standard_face_order = ['white', 'red', 'green', 'yellow', 'orange', 'blue']
            
            combined_string = []
            for side_color in standard_face_order:
                if side_color in notation:
                    face_string = ''.join(notation[side_color])
                    if len(face_string) == 9:  # Each face should have 9 stickers
                        combined_string.append(face_string)
                    else:
                        print(f"ERROR: Face '{side_color}' has {len(face_string)} stickers, expected 9.")
                        return ""
                else:
                    # If a face wasn't scanned, we cannot generate a valid string.
                    print(f"ERROR: Face '{side_color}' was not scanned. Cannot generate valid cube string.")
                    return ""
            
            result = "".join(combined_string)
            if len(result) == 54:
                return result
            else:
                print(f"ERROR: Generated string has {len(result)} characters, expected 54.")
                return ""
                
        except Exception as e:
            print(f"ERROR in get_result_notation: {e}")
            return ""

    def state_already_solved(self):
        """Check if the scanned cube is already in solved state."""
        solved_state = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
        current_notation = self.get_result_notation()
        return current_notation == solved_state

    def run(self):
        """
        Open up the webcam and present the user with the Qbr user interface.

        Returns a string of the scanned state in rubik's cube notation.
        """
        # Set up mouse callback for manual correction
        cv2.namedWindow("AeroHack 2025 - Professional Rubik's Cube Solver")
        cv2.setMouseCallback("AeroHack 2025 - Professional Rubik's Cube Solver", self.mouse_callback)
        
        while True:
            _, frame = self.cam.read()
            self.frame = frame
            key = cv2.waitKey(10) & 0xff

            # Quit on escape.
            # Check for escape key
            escape_key = self.controls_config.get('escape_key', 27)
            if key == escape_key:
                break

            # Toggle manual correction mode with 'M' key
            if key == ord('m') or key == ord('M'):
                self.manual_correction_mode = not self.manual_correction_mode
                print(f"Manual correction mode: {'ON' if self.manual_correction_mode else 'OFF'}")
                
                # When entering manual correction mode, ensure preview_state contains valid BGR tuples
                if self.manual_correction_mode:
                    for i in range(len(self.preview_state)):
                        if not isinstance(self.preview_state[i], (tuple, list)) or len(self.preview_state[i]) != 3:
                            self.preview_state[i] = (255, 255, 255)  # Default to white BGR

            if not self.calibrate_mode and not self.manual_correction_mode:
                # Update the snapshot when space bar is pressed.
                # Check for space key
                space_key = self.controls_config.get('space_key', 32)
                if key == space_key:
                    self.update_snapshot_state()

                # Switch to another language.
                if key == ord(SWITCH_LANGUAGE_KEY):
                    next_locale = get_next_locale(config.get_setting('locale', 'en'))
                    config.set_setting('locale', next_locale)

            # Toggle calibrate mode (disable if in manual correction mode).
            if key == ord(CALIBRATE_MODE_KEY) and not self.manual_correction_mode:
                self.reset_calibrate_mode()
                self.calibrate_mode = not self.calibrate_mode

            # Color override shortcuts during calibration mode
            if self.calibrate_mode and not self.done_calibrating:
                # Ctrl+W to force white color during calibration
                if key == 23:  # Ctrl+W (ASCII code for Ctrl+W)
                    self.force_calibrate_color('white')
                # Ctrl+R to force red color during calibration  
                elif key == 18:  # Ctrl+R
                    self.force_calibrate_color('red')
                # Ctrl+G to force green color during calibration
                elif key == 7:   # Ctrl+G
                    self.force_calibrate_color('green')
                # Ctrl+Y to force yellow color during calibration
                elif key == 25:  # Ctrl+Y
                    self.force_calibrate_color('yellow')
                # Ctrl+O to force orange color during calibration
                elif key == 15:  # Ctrl+O
                    self.force_calibrate_color('orange')
                # Ctrl+B to force blue color during calibration
                elif key == 2:   # Ctrl+B
                    self.force_calibrate_color('blue')

            grayFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            blurredFrame = cv2.blur(grayFrame, (3, 3))
            cannyFrame = cv2.Canny(blurredFrame, 30, 60, 3)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
            dilatedFrame = cv2.dilate(cannyFrame, kernel)

            contours = self.find_contours(dilatedFrame)
            if len(contours) == 9:
                self.draw_contours(contours)
                if not self.calibrate_mode:
                    self.update_preview_state(contours)
                elif key == 32 and self.done_calibrating is False:
                    current_color = self.colors_to_calibrate[self.current_color_to_calibrate_index]
                    (x, y, w, h) = contours[4]
                    roi = self.frame[y+7:y+h-7, x+14:x+w-14]
                    avg_bgr = color_detector.get_dominant_color(roi)
                    self.calibrated_colors[current_color] = avg_bgr
                    self.current_color_to_calibrate_index += 1
                    self.done_calibrating = self.current_color_to_calibrate_index == len(self.colors_to_calibrate)
                    if self.done_calibrating:
                        color_detector.set_cube_color_pallete(self.calibrated_colors)
                        config.set_setting(CUBE_PALETTE, color_detector.cube_color_palette)

            if self.calibrate_mode:
                self.draw_current_color_to_calibrate()
                self.draw_calibrated_colors()
            elif self.manual_correction_mode:
                self.draw_manual_correction_instructions()
                self.draw_preview_stickers()
                self.draw_snapshot_stickers()
                self.draw_scanned_sides()
                self.draw_2d_cube_state()
            else:
                self.draw_current_language()
                self.draw_preview_stickers()
                self.draw_snapshot_stickers()
                self.draw_scanned_sides()
                self.draw_2d_cube_state()

            cv2.imshow("AeroHack 2025 - Professional Rubik's Cube Solver", self.frame)

        self.cam.release()
        cv2.destroyAllWindows()

        if len(self.result_state.keys()) != 6:
            return E_INCORRECTLY_SCANNED

        if not self.scanned_successfully():
            return E_INCORRECTLY_SCANNED

        if self.state_already_solved():
            return E_ALREADY_SOLVED

        return self.get_result_notation()


webcam = Webcam()
