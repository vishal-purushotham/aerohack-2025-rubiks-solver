# FILE: src/python/simulation_server.py
# Clean, updated server implementation

from flask import Flask, jsonify, send_from_directory
import webbrowser
import threading
import os
import logging

# --- Flask App Setup ---
frontend_folder = os.path.join(os.path.dirname(__file__), 'frontend')
app = Flask(__name__, static_folder=frontend_folder, template_folder=frontend_folder)

# Disable Flask's production warning
logging.getLogger('werkzeug').setLevel(logging.ERROR)

# --- Global Data Store ---
CUBE_DATA = {
    "state": "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB",
    "solution": ""
}

# --- API Endpoints ---
@app.route('/')
def serve_index():
    """Serves the main HTML file."""
    return send_from_directory(frontend_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serves static files like main.js and cube.js."""
    return send_from_directory(frontend_folder, filename)

@app.route('/get_cube_data')
def get_cube_data():
    """Provides the cube state and solution to the frontend."""
    print(f"Sending cube data: {CUBE_DATA}")
    return jsonify(CUBE_DATA)

# --- Server Control ---
def run_simulation(state, solution):
    """Starts the Flask server and opens the simulation in a browser."""
    global CUBE_DATA
    
    # Clean up solution string (remove timing info)
    if solution and "(" in solution:
        solution = solution.split("(")[0].strip()
    
    CUBE_DATA['state'] = state
    CUBE_DATA['solution'] = solution
    
    print(f"Cube state: {state}")
    print(f"Solution: {solution}")
    
    url = "http://127.0.0.1:5000"
    print(f"🚀 Launching 3D simulation at {url}")
    
    # Open browser after a slight delay to ensure server is ready
    threading.Timer(1.5, lambda: webbrowser.open(url)).start()
    
    # Run Flask with minimal output
    app.run(port=5000, debug=False, use_reloader=False)