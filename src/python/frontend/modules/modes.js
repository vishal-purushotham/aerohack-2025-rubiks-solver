// src/python/frontend/modules/modes.js

import { initMotions } from './animations.js';
import { disableManualButtons, toggleShowDirection } from "./ui.js";

let mode = { autoSolve: false, reverse: false };
export function isAutoSolveMode() { return mode.autoSolve === true; }
export function isReverseMode() { return mode.reverse === true; }
export function resetMode() { setAutoSolve(false); setReverse(false); }

export function setAutoSolve(autoSolve) {
    mode.autoSolve = autoSolve;
    disableManualButtons(autoSolve);
}

export function setReverse(reverse = null) {
    mode.reverse = reverse === null ? !mode.reverse : reverse;
    initMotions(!mode.reverse);
    if (!mode.autoSolve) toggleShowDirection(!mode.reverse);
}
window.setReverse = setReverse; // Make it accessible from HTML onclick
