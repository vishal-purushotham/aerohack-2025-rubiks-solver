# In src/python/simulation_server.py (REPLACE ENTIRE FILE)

from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import webbrowser
import threading
import os
import logging

# --- Flask App Setup ---
frontend_folder = os.path.join(os.path.dirname(__file__), 'frontend')
app = Flask(__name__, static_folder=None)
CORS(app)

# Suppress noisy Flask logging to keep the console clean
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# This is a simple, robust way to hold the state for the session.
# It will be populated by the run_simulation function.
SESSION_DATA = {
    "state": "",
    "solution": ""
}

# --- API ENDPOINTS ---
# These endpoints now read from the SESSION_DATA dictionary,
# which is guaranteed to be populated before the server starts accepting requests.

@app.route('/')
def serve_index():
    return send_from_directory(frontend_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory(frontend_folder, filename)

@app.route('/modules/<path:filename>')
def serve_modules(filename):
    return send_from_directory(os.path.join(frontend_folder, 'modules'), filename)

@app.route('/get_cube_data')
def get_cube_data():
    # This will now correctly return the data set by run_simulation
    return jsonify(SESSION_DATA)

@app.route('/move', methods=['POST'])
def apply_move():
    # This server is stateless for moves, which is fine. The frontend handles visuals.
    move = request.json.get('move')
    return jsonify({"status": "ok", "move": move})

@app.route('/solve')
def solve_cube():
    solution_str = SESSION_DATA.get("solution", "")
    # The frontend expects a 'parsedMoves' array.
    # We correctly split moves like R2 into two separate moves.
    parsed_moves = []
    if solution_str:
        for move in solution_str.split():
            if "2" in move:
                base_move = move.replace("2", "")
                parsed_moves.extend([base_move, base_move])
            else:
                parsed_moves.append(move)

    return jsonify({
        "solutionString": solution_str,
        "parsedMoves": parsed_moves
    })

@app.route('/reset-cube', methods=['POST'])
def reset_cube_state():
    # This endpoint is kept for consistency, though the frontend reset handles the visuals.
    return jsonify({"status": "reset"})

# --- SERVER CONTROL ---
def run_simulation(state, solution):
    """
    Populates the session data and runs the Flask server.
    This function is the single entry point for starting a simulation.
    """
    global SESSION_DATA

    # Clean up the solution string to remove timing info for the frontend
    if solution and "(" in solution:
        solution = solution.split("(")[0].strip()

    # **CRITICAL FIX**: Populate the state *before* starting the server thread.
    SESSION_DATA['state'] = state
    SESSION_DATA['solution'] = solution

    url = "http://127.0.0.1:5000"
    print(f"🚀 Launching 3D simulation at {url}")
    
    # Open the browser after a short delay to ensure the server is ready
    threading.Timer(1.25, lambda: webbrowser.open(url)).start()

    # Run the Flask app. This is a blocking call.
    app.run(port=5000, debug=False, use_reloader=False)