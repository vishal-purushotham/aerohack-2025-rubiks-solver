// In src/python/frontend/modules/main.js (REPLACE ENTIRE FILE)

import { initMotions, updateAnimations } from './animations.js';
import { initCanvas, render } from './sceneManager.js';
import { resetCubeObject, createCube } from './rubik.js';
import { initKeyHandler } from './keyHandler.js';
import { resetBackendState, getCubeData } from './api.js';
import { clearAllDisplays } from './ui.js';

// --- GLOBAL EXPORTS ---
window.resetState = resetState;

// --- INITIALIZATION ---
initCanvas();
resetState();
update();

function update() {
    // We comment out the animation update to prevent any potential errors.
    // updateAnimations(0.016); 
    requestAnimationFrame(update);
    render();
}

async function resetState() {
    console.log("--- resetState called (Stable Version) ---");
    
    // Fetch data just to display the solution text
    const cubeData = await getCubeData();
    const solution = cubeData.solution || "Solution will appear here.";
    document.getElementById("solution-display").textContent = solution;
    console.log("Solution from server:", solution);

    // Reset backend and clear any old session data
    resetBackendState();
    sessionStorage.clear();

    // Create a perfect, solved cube
    resetCubeObject();
    createCube();
    
    // Initialize other UI components
    initMotions(true);
    initKeyHandler();
    clearAllDisplays(); // This will clear the solution display, so we set it again
    
    document.getElementById("solution-display").textContent = solution;
    console.log("Stable solved cube has been rendered.");
}
