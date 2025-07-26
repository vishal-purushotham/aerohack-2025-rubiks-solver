import { cube } from "./main.js";

export const Faces = Object.freeze({
    R: "R",
    L: "L",
    U: "U",
    D: "D",
    F: "F",
    B: "B",
});

const faceMap = {
    'r': Faces.R,
    'l': Faces.L,
    'u': Faces.U,
    'd': Faces.D,
    'f': Faces.F,
    'b': Faces.B,
};

export function getFace(key) {
    return faceMap[key.toLowerCase()];
}

export function animate(face, direction) {
    return new Promise(resolve => {
        if (cube && !cube.isRotating) {
            cube.rotateFace(face, direction, resolve);
        } else {
            resolve(); // Resolve immediately if cube is not ready or already rotating
        }
    });
}

// No longer needed, cube handles its own animation updates
export function updateAnimations() {}
export function initMotions() {}
