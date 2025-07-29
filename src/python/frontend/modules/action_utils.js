// src/python/frontend/modules/action_utils.js

import { isReverseMode, setAutoSolve, setReverse } from './modes.js';
import { postMove } from './api.js';
import { handleMove } from './keyHandler.js';

export async function saveMove(move, session) {
  if (session) {
    let historyString = sessionStorage.getItem("keyEventHistory");
    let history = historyString ? JSON.parse(historyString) : [];
    if (history.length > 50) history.shift();
    history.push(move);
    sessionStorage.setItem("keyEventHistory", JSON.stringify(history));
  }
  await postMove(move);
}

export async function undoLastMove() {
    let historyString = sessionStorage.getItem("keyEventHistory");
    if (!historyString) return;
    let history = JSON.parse(historyString);
    if (history.length > 0) {
        let lastMove = history.pop();
        let oppMove = lastMove.endsWith("'") ? lastMove.slice(0, -1) : (lastMove.endsWith("2") ? lastMove : lastMove + "'");
        sessionStorage.setItem("keyEventHistory", JSON.stringify(history));
        await makeAutoMove(oppMove, false);
    }
}
window.undoLastMove = undoLastMove;

export async function makeAutoMove(move, saveSession) {
  const prevReverseMode = isReverseMode();
  let success;
  try {
    setAutoSolve(true);
    await handleMove(move, saveSession);
    setReverse(prevReverseMode);
    setAutoSolve(false);
    success = true;
  }
  catch (error) {
    console.error("Error executing auto-move:", error);
    setReverse(prevReverseMode);
    setAutoSolve(false);
    success = false;
  }
  return success;
}
