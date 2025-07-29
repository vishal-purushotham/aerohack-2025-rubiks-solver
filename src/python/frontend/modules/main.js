// In src/python/frontend/modules/main.js (REPLACE ENTIRE FILE)

import { initMotions, updateAnimations } from './animations.js';
import { initCanvas, render } from './sceneManager.js';
import { resetCubeObject, createCube, applyMove } from './rubik.js';
import { initKeyHandler } from './keyHandler.js';
import { resetBackendState, getCubeData } from './api.js';
import { clearAllDisplays } from './ui.js';
import { getInverseSolution } from './solutionService.js';

// --- GLOBAL EXPORTS ---
window.resetState = resetState;

// --- INITIALIZATION ---
initCanvas();
resetState();
update();

function update() {
    // The animation update is for the solver animation, not the setup.
    // It's fine to leave it here.
    updateAnimations(0.016); 
    requestAnimationFrame(update);
    render();
}

async function resetState() {
    console.log("--- resetState called ---");
    sessionStorage.clear();
    
    const cubeData = await getCubeData();
    console.log("1. Received cube data from server:", JSON.stringify(cubeData));
    
    resetBackendState();
    resetCubeObject();
    createCube(); // This now creates a correctly colored solved cube
    initMotions(true);
    initKeyHandler();
    clearAllDisplays();
    
    const solution = cubeData.solution || "";
    document.getElementById("solution-display").textContent = solution;
    console.log("2. Solution string to be inverted:", solution);

    const scrambleMoves = getInverseSolution(solution);
    console.log("3. Calculated scramble (inverse solution):", scrambleMoves);

    if (scrambleMoves.length === 0 && solution.length > 0) {
        console.error("Scramble calculation failed. Solution was present but inverse is empty.");
    } else if (scrambleMoves.length === 0) {
        console.warn("No scramble moves to apply. Cube will remain solved.");
    } else {
        console.log("4. Applying scramble moves instantly...");
        scrambleMoves.forEach(move => {
            applyMove(move);
        });
        console.log("5. Scramble complete. The cube should now appear scrambled.");
    }
}
