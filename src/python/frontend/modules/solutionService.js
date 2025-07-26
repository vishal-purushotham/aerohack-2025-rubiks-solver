import { resetMode } from './modes.js';
import { makeAutoMove } from './action_utils.js'; 
import { getSolution } from './api.js';


// TODO: Refactor to separate getting solution, animating, and handling display
export async function handleSolve() {
    const solutionDisplay = document.getElementById("solution-display");
    solutionDisplay.textContent = "";

    let data = await getSolution();
    let solutionString = null;
    let parsedMoves = null;

    // Try to use the expected structure from /solve
    if (data && data.solutionString && data.parsedMoves) {
        solutionString = data.solutionString;
        parsedMoves = data.parsedMoves;
    } else if (data && data.solution) {
        // Fallback: if only a solution string is returned
        solutionString = data.solution;
        parsedMoves = solutionString.trim().split(/\s+/);
    } else {
        // Fallback: fetch from /get_cube_data
        const cubeData = await fetch('/get_cube_data').then(r => r.json());
        solutionString = cubeData.solution;
        parsedMoves = solutionString.trim().split(/\s+/);
    }

    let i = 0;
    async function nextMove() {
        if (!parsedMoves || parsedMoves.length === 0) return;
        if (i < parsedMoves.length) {
            const move = parsedMoves[i];
            solutionDisplay.textContent += " " + move;
            await makeAutoMove(move, true);
            i++;
            nextMove();
        } else {
            resetMode();
        }
    }
    nextMove();
}

