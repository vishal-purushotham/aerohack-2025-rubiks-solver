import './modes.js'; // defines the different operational modes of the app
import {initMotions, updateAnimations} from './animations.js'; // defines face rotation animations
import {initCanvas} from './sceneManager.js'; // sets up the canvas and asynchronously renders the scene using an update callback
import { resetCubeObject} from './rubik.js'; // defines the cube and its actions
import './action_utils.js'; // manages user interactions, performs moves, and displays action info on the GUI
import { initKeyHandler } from './keyHandler.js';
import { handleSolve } from './solutionService.js'; // implements functions for autosolve mode
import { render } from './sceneManager.js';
import { resetMode } from './modes.js';
import { resetBackendState, getCubeData } from './api.js';
import { clearAllDisplays } from './ui.js';


initCanvas();
document.getElementById('solve-button').addEventListener('click', handleSolve);
resetState();

// update callback
async function update() {
    updateAnimations();
    requestAnimationFrame(update); // requests the next update call; this creates a loop
    render();
}
update();

export async function resetState() {
    resetBackendState();
    sessionStorage.clear();
    const cubeData = await getCubeData();
    resetCubeObject(cubeData);
    initMotions(true);
    initKeyHandler();
    resetMode();
    clearAllDisplays();
}
window.resetState = resetState;
