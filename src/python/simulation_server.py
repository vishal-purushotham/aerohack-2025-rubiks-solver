# FILE: src/python/simulation_server.py
# ACTION: Replace the entire file with this corrected version.

from flask import Flask, jsonify, send_from_directory
import webbrowser
import threading
import os

# --- Flask App Setup ---
frontend_folder = os.path.join(os.path.dirname(__file__), 'frontend')
# IMPORTANT: Explicitly set the static folder for Flask to serve JS correctly.
app = Flask(__name__, static_folder=frontend_folder, template_folder=frontend_folder)

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
    """Serves static files like main.js."""
    return send_from_directory(frontend_folder, filename)

@app.route('/get_cube_data')
def get_cube_data():
    """Provides the cube state and solution to the frontend."""
    return jsonify(CUBE_DATA)

# --- Server Control ---
def run_simulation(state, solution):
    """Starts the Flask server and opens the simulation in a browser."""
    global CUBE_DATA
    CUBE_DATA['state'] = state
    CUBE_DATA['solution'] = solution
    
    url = "http://127.0.0.1:5000"
    print(f"🚀 Launching 3D simulation at {url}")
    
    threading.Timer(1.25, lambda: webbrowser.open(url)).start()
    
    app.run(port=5000, debug=False, use_reloader=False)
