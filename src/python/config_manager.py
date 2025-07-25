#!/usr/bin/env python3
"""
Configuration Management for AeroHack Rubik's Cube Solver
Eliminates hardcoded values throughout the system
"""

import json
import os
from typing import Dict, Any, Optional


class ConfigManager:
    """Centralized configuration management to eliminate hardcoded values."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager."""
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Config file {self.config_path} not found. Using defaults.")
            return self._get_default_config()
        except json.JSONDecodeError as e:
            print(f"Error parsing config file: {e}. Using defaults.")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Provide default configuration values."""
        return {
            "solver": {
                "max_length": 25,
                "timeout_seconds": 10,
                "cube_string_length": 54
            },
            "camera": {
                "detection": {
                    "min_aspect_ratio": 0.8,
                    "max_aspect_ratio": 1.2,
                    "min_sticker_width": 30,
                    "max_sticker_width": 60,
                    "min_area_ratio": 0.4,
                    "contour_approx_vertices": 4
                },
                "calibration": {
                    "neighbor_search_radius": 1.5,
                    "expected_neighbors": 9,
                    "expected_stickers_per_color": 9
                },
                "ui": {
                    "text_offset_y": 20,
                    "color_grid_x1": 90,
                    "corner_text_offset": 20,
                    "stroke_width": 1
                },
                "controls": {
                    "escape_key": 27,
                    "space_key": 32
                }
            },
            "performance": {
                "initial_solve_time": 0.0,
                "memory_unit": "MB",
                "stats_filename": "performance_stats.json"
            },
            "colors": {
                "expected_faces": 6,
                "stickers_per_face": 9,
                "total_stickers": 54
            }
        }
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path (e.g., 'solver.max_length')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        try:
            keys = key_path.split('.')
            value = self.config
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> None:
        """
        Set configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path (e.g., 'solver.max_length')
            value: Value to set
        """
        keys = key_path.split('.')
        config_section = self.config
        
        # Navigate to parent
        for key in keys[:-1]:
            if key not in config_section:
                config_section[key] = {}
            config_section = config_section[key]
        
        # Set the value
        config_section[keys[-1]] = value
    
    def save(self) -> None:
        """Save current configuration to file."""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def reload(self) -> None:
        """Reload configuration from file."""
        self.config = self._load_config()


# Global configuration instance
config = ConfigManager()


# Convenience functions for common operations
def get_solver_config() -> Dict[str, Any]:
    """Get solver configuration."""
    return config.get('solver', {})


def get_camera_config() -> Dict[str, Any]:
    """Get camera configuration."""
    return config.get('camera', {})


def get_performance_config() -> Dict[str, Any]:
    """Get performance configuration."""
    return config.get('performance', {})


def get_colors_config() -> Dict[str, Any]:
    """Get colors configuration."""
    return config.get('colors', {})
