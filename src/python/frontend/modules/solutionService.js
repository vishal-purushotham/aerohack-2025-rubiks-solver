// src/python/frontend/modules/solutionService.js
import { resetMode } from './modes.js';
import { makeAutoMove } from './action_utils.js';
import { getSolution } from './api.js';

window.handleSolve = handleSolve;

export async function handleSolve() {
    const solutionDisplay = document.getElementById("solution-display");
    const data = await getSolution();

    if (!data || !data.solutionString) {
        solutionDisplay.textContent = "No solution found or error occurred.";
        return;
    }
    
    solutionDisplay.textContent = data.solutionString;
    const parsedMoves = data.parsedMoves || data.solutionString.split(' ').filter(m => m);
    
    if (parsedMoves.length === 0 || parsedMoves[0] === '' || data.solutionString.toLowerCase().includes("solved")) {
        return;
    }

    let i = 0;
    async function nextMove() {
        if (i >= parsedMoves.length) {
            resetMode();
            return;
        }
        const move = parsedMoves[i];
        if (move) {
            await makeAutoMove(move, false);
        }
        i++;
        setTimeout(nextMove, 50);
    }
    nextMove();
}

export function getInverseSolution(solution) {
    if (!solution || solution.toLowerCase().includes("solved")) return [];
    return solution.split(' ').filter(m => m).reverse().map(move => {
        if (move.includes("'")) return move.replace("'", "");
        if (move.includes("2")) return move; // The inverse of a 180-degree turn is the same turn
        return move + "'";
    });
}
