#!/usr/bin/env python3
"""
Performance Monitor for AeroHack 2025 Rubik's Cube Solver
Tracks solve times, move counts, and system performance
"""

import time
import json
import psutil
from datetime import datetime
from typing import Dict, List, Optional

class PerformanceMonitor:
    """Monitor and track solver performance metrics."""
    
    def __init__(self):
        """Initialize the performance monitor."""
        self.stats = {
            'solve_times': [],
            'move_counts': [],
            'memory_usage': [],
            'cpu_usage': [],
            'timestamps': []
        }
        self.current_solve_start = None
        self.session_start = time.time()
    
    def start_solve_timing(self):
        """Start timing a solve operation."""
        self.current_solve_start = time.time()
        
        # Record system state
        try:
            process = psutil.Process()
            self.start_memory = process.memory_info().rss / 1024 / 1024  # MB
        except:
            self.start_memory = 0
    
    def end_solve_timing(self, solution: str) -> Dict:
        """
        End timing and record solve statistics.
        
        Args:
            solution: The solution string from the solver
            
        Returns:
            Dictionary with solve statistics
        """
        if self.current_solve_start is None:
            return {}
        
        solve_time = time.time() - self.current_solve_start
        
        # Parse move count from solution
        move_count = self.parse_move_count(solution)
        
        # Record system metrics
        try:
            process = psutil.Process()
            end_memory = process.memory_info().rss / 1024 / 1024  # MB
            cpu_percent = psutil.cpu_percent(interval=0.1)
        except:
            end_memory = 0
            cpu_percent = 0
        
        # Store statistics
        self.stats['solve_times'].append(solve_time)
        self.stats['move_counts'].append(move_count)
        self.stats['memory_usage'].append(end_memory)
        self.stats['cpu_usage'].append(cpu_percent)
        self.stats['timestamps'].append(datetime.now().isoformat())
        
        solve_stats = {
            'solve_time': solve_time,
            'move_count': move_count,
            'memory_mb': end_memory,
            'cpu_percent': cpu_percent,
            'timestamp': self.stats['timestamps'][-1]
        }
        
        self.current_solve_start = None
        return solve_stats
    
    def parse_move_count(self, solution: str) -> int:
        """Extract move count from solution string."""
        if not solution or solution.startswith("Error"):
            return 0
        
        try:
            # Look for pattern like "(20f)" or similar
            if '(' in solution and ')' in solution:
                info = solution.split('(')[1].split(')')[0]
                if 'f' in info:
                    return int(info.replace('f', '').strip())
            
            # Fallback: count space-separated moves
            moves = solution.strip().split()
            # Filter out timing information
            move_count = 0
            for move in moves:
                if move and not move.startswith('(') and not 's' in move:
                    move_count += 1
            
            return move_count
        except:
            return 0
    
    def get_current_stats(self) -> Dict:
        """Get current session statistics."""
        if not self.stats['solve_times']:
            return {
                'total_solves': 0,
                'session_time': time.time() - self.session_start
            }
        
        return {
            'total_solves': len(self.stats['solve_times']),
            'avg_solve_time': sum(self.stats['solve_times']) / len(self.stats['solve_times']),
            'min_solve_time': min(self.stats['solve_times']),
            'max_solve_time': max(self.stats['solve_times']),
            'avg_move_count': sum(self.stats['move_counts']) / len(self.stats['move_counts']) if self.stats['move_counts'] else 0,
            'min_move_count': min(self.stats['move_counts']) if self.stats['move_counts'] else 0,
            'max_move_count': max(self.stats['move_counts']) if self.stats['move_counts'] else 0,
            'avg_memory_mb': sum(self.stats['memory_usage']) / len(self.stats['memory_usage']) if self.stats['memory_usage'] else 0,
            'avg_cpu_percent': sum(self.stats['cpu_usage']) / len(self.stats['cpu_usage']) if self.stats['cpu_usage'] else 0,
            'session_time': time.time() - self.session_start
        }
    
    def get_performance_summary(self) -> str:
        """Get a formatted performance summary."""
        stats = self.get_current_stats()
        
        if stats['total_solves'] == 0:
            return "No solves recorded yet."
        
        summary = f"""
Performance Summary:
===================
Total Solves: {stats['total_solves']}
Session Time: {stats['session_time']:.1f}s

Solve Times:
  Average: {stats['avg_solve_time']:.3f}s
  Fastest: {stats['min_solve_time']:.3f}s
  Slowest: {stats['max_solve_time']:.3f}s

Move Counts:
  Average: {stats['avg_move_count']:.1f}
  Minimum: {stats['min_move_count']}
  Maximum: {stats['max_move_count']}

System Usage:
  Memory: {stats['avg_memory_mb']:.1f} MB
  CPU: {stats['avg_cpu_percent']:.1f}%
"""
        return summary
    
    def save_stats(self, filename: str = 'performance_stats.json'):
        """Save performance statistics to file."""
        try:
            data = {
                'session_info': {
                    'start_time': datetime.fromtimestamp(self.session_start).isoformat(),
                    'end_time': datetime.now().isoformat(),
                    'duration_seconds': time.time() - self.session_start
                },
                'statistics': self.get_current_stats(),
                'raw_data': self.stats
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"📊 Performance data saved to {filename}")
            return True
        except Exception as e:
            print(f"❌ Failed to save performance data: {e}")
            return False
    
    def load_stats(self, filename: str = 'performance_stats.json') -> bool:
        """Load performance statistics from file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            if 'raw_data' in data:
                self.stats = data['raw_data']
                print(f"📊 Performance data loaded from {filename}")
                return True
            else:
                print(f"❌ Invalid performance data format in {filename}")
                return False
        except FileNotFoundError:
            print(f"📊 No existing performance data found at {filename}")
            return False
        except Exception as e:
            print(f"❌ Failed to load performance data: {e}")
            return False
    
    def reset_stats(self):
        """Reset all performance statistics."""
        self.stats = {
            'solve_times': [],
            'move_counts': [],
            'memory_usage': [],
            'cpu_usage': [],
            'timestamps': []
        }
        self.session_start = time.time()
        print("📊 Performance statistics reset")

# Global performance monitor instance
perf_monitor = PerformanceMonitor()

if __name__ == "__main__":
    """Generate sample performance data and save to JSON file."""
    import random
    
    print("🎯 Generating sample performance data...")
    
    # Simulate 1000 solve sessions with realistic data
    for i in range(1000):
        # Start timing
        perf_monitor.start_solve_timing()
        
        # Simulate solve time (0.5 to 5.0 seconds)
        solve_time = random.uniform(0.5, 5.0)
        time.sleep(0.001)  # Smaller delay to speed up generation
        
        # Generate realistic solution string with move count
        move_count = random.randint(15, 25)
        sample_moves = ["R", "U", "R'", "U'", "F", "D", "L", "B", "D'", "F'", "L'", "B'"]
        solution = " ".join(random.choices(sample_moves, k=move_count))
        solution += f" ({move_count}f)"
        
        # Record the solve
        stats = perf_monitor.end_solve_timing(solution)
        
        if i % 100 == 0:
            print(f"  Generated {i+1}/1000 solve records...")
    
    print("\n" + perf_monitor.get_performance_summary())
    
    # Save to JSON file
    filename = 'performance_stats.json'
    if perf_monitor.save_stats(filename):
        print(f"\n✅ Performance data saved to {filename}")
        print("📊 You can now create histograms from this data!")
        
        # Show what data is available
        stats = perf_monitor.get_current_stats()
        print(f"\nData available for histograms:")
        print(f"  - Solve times: {len(perf_monitor.stats['solve_times'])} values")
        print(f"  - Move counts: {len(perf_monitor.stats['move_counts'])} values")
        print(f"  - Memory usage: {len(perf_monitor.stats['memory_usage'])} values")
        print(f"  - CPU usage: {len(perf_monitor.stats['cpu_usage'])} values")
    else:
        print("\n❌ Failed to save performance data")
