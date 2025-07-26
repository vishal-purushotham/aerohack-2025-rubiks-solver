import { displayMove, showAlert } from "./ui.js";
import { saveMove, undoLastMove } from "./action_utils.js";
import { isAutoSolveMode, isReverseMode, setReverse } from "./modes.js";
import { animate, getFace } from "./animations.js";

const keyMap = {
    'R': 'R', 'L': 'L', 'U': 'U', 'D': 'D', 'F': 'F', 'B': 'B',
    '1': '1', '2': '2', 'Z': 'Z'
};
  
let lastKeyTime = 0;
const keyCooldown = 100;
async function onDocumentKeyDown(event) {
    const key = event.key.toUpperCase();
    const move = keyMap[key];

    if (!move) return; // Ignore non-relevant keys

    const currentTime = Date.now();
    if (!event.ctrlKey && move !== '1' && move !== '2' && (currentTime - lastKeyTime < keyCooldown)) {
        showAlert("Too quick!", "in cooldown.");
        return;
    }
    lastKeyTime = currentTime;

    if (isAutoSolveMode() && !['1', '2', 'Z'].includes(move)) {
        showAlert("In autosolve mode:", "manual moves are temporarily disabled.");
        return;
    }

    if (event.ctrlKey && move === 'Z') {
        undoLastMove();
        return;
    }

    if (move === '1') {
        setReverse(false);
        return;
    }

    if (move === '2') {
        setReverse(true);
        return;
    }

    if (['R', 'L', 'U', 'D', 'F', 'B'].includes(move)) {
        const finalMove = isReverseMode() ? move + "'" : move;
        handleMove(finalMove, true);
    }
};

export function initKeyHandler() {
  document.addEventListener("keydown", onDocumentKeyDown, false);
}

export async function handleMove(move, saveSession) {
    try {
        const face = getFace(move.charAt(0));
        const isClockwise = !move.includes("'");

        if (!face) return false;

        await Promise.all([
            displayMove(move),
            animate(face, isClockwise),
            saveMove(move, saveSession)
        ]);
        return true;
    } catch (error) {
        console.error("Error handling move action:", error);
        return false;
    }
}
