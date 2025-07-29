// src/python/frontend/modules/keyHandler.js

import { displayMove, showAlert } from "./ui.js";
import { saveMove, undoLastMove } from "./action_utils.js";
import { isAutoSolveMode, isReverseMode, setReverse } from "./modes.js";
import { animate, Faces } from "./animations.js";

const keyMap = {
    'R': { face: Faces.RIGHT }, 'L': { face: Faces.LEFT }, 'M': { face: Faces.MID },
    'U': { face: Faces.UP }, 'D': { face: Faces.DOWN }, 'F': { face: Faces.FRONT },
    'B': { face: Faces.BACK }, '1': {}, '2': {}, 'Z': {}
};

let lastKeyTime = 0;
const keyCooldown = 350; // ms, adjusted to match animation duration

async function onDocumentKeyDown(event) {
    const key = event.key.toUpperCase();
    if (!keyMap[key]) return;

    const currentTime = Date.now();
    if (!event.ctrlKey && !['1', '2'].includes(key) && (currentTime - lastKeyTime < keyCooldown)) {
        showAlert("Animation in progress...");
        return;
    }
    lastKeyTime = currentTime;

    if (isAutoSolveMode() && !['1', '2', 'Z'].includes(key)) {
        showAlert("Solver is running. Manual moves disabled.");
        return;
    }
    if (event.ctrlKey && key === 'Z') {
        undoLastMove();
        return;
    }
    if (key === '1') { setReverse(false); return; }
    if (key === '2') { setReverse(true); return; }

    const finalMove = isReverseMode() ? key + "'" : key;
    handleMove(finalMove, true);
}

export function initKeyHandler() {
  document.addEventListener("keydown", onDocumentKeyDown, false);
}

export async function handleMove(move, saveSession) {
    const faceChar = move.charAt(0).toUpperCase();
    const keyAction = keyMap[faceChar];
    if (!keyAction || !keyAction.face) return false;

    setReverse(move.includes("'"));

    try {
        await Promise.all([
            displayMove(move),
            animate(keyAction.face),
            saveMove(move, saveSession)
        ]);
        return true;
    } catch (error) {
        console.error("Error handling move action:", error);
        return false;
    }
}
