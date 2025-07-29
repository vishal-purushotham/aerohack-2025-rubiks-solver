// src/python/frontend/modules/ui.js

import { duration } from "./animations.js";

export function showAlert(message) {
    const container = document.getElementById('messages-container');
    if (!container) return;
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert';
    alertDiv.innerHTML = `<strong>Info:</strong> ${message}`;
    container.appendChild(alertDiv);
    setTimeout(() => {
        alertDiv.classList.add('fade-out');
        alertDiv.addEventListener('transitionend', () => alertDiv.remove());
    }, 1500);
}

export function displayMove(move) {
    // This UI element doesn't exist in the new HTML, but we keep the function
    // in case you want to add it back. It won't cause an error.
    const actionDisplay = document.getElementById("action-display");
    if (actionDisplay) {
        actionDisplay.textContent = move;
        setTimeout(() => { actionDisplay.textContent = ""; }, duration * 1000 + 100);
    }
}

export function toggleShowDirection(clockwise) {
    // This UI element doesn't exist in the new HTML.
}

export function disableManualButtons(disable) {
    document.getElementById("solve-button").disabled = disable;
    document.getElementById("reset-button").disabled = disable;
}

export function clearAllDisplays() {
    const solutionDisplay = document.getElementById("solution-display");
    if (solutionDisplay) solutionDisplay.textContent = "";
}
