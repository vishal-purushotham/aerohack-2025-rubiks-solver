// In src/python/frontend/modules/rubik.js (REPLACE ENTIRE FILE)

import { scene } from './sceneManager.js';

let cubesArray3D = []; // This will hold the logical state [x][y][z] of the cubelets

// Standard Western Color Scheme: U=White, F=Green, R=Red
const materials = {
    'U': new THREE.MeshBasicMaterial({ color: 0xFFFFFF, side: THREE.DoubleSide }), // White
    'D': new THREE.MeshBasicMaterial({ color: 0xFFD700, side: THREE.DoubleSide }), // Yellow
    'L': new THREE.MeshBasicMaterial({ color: 0xFF8C00, side: THREE.DoubleSide }), // Orange
    'R': new THREE.MeshBasicMaterial({ color: 0xB71C1C, side: THREE.DoubleSide }), // Red
    'F': new THREE.MeshBasicMaterial({ color: 0x009A44, side: THREE.DoubleSide }), // Green
    'B': new THREE.MeshBasicMaterial({ color: 0x003DA5, side: THREE.DoubleSide }), // Blue
    'black': new THREE.MeshBasicMaterial({ color: 0x222222, side: THREE.DoubleSide })
};

function generateMaterial(x, y, z) {
    if (x === 1 && y === 1 && z === 1) return materials.black; // Center piece is hidden
    
    // Maps world coordinates to faces
    const materialArray = [
        (x === 2) ? materials.R : materials.black, // Right (+X)
        (x === 0) ? materials.L : materials.black, // Left (-X)
        (y === 2) ? materials.U : materials.black, // Up (+Y)
        (y === 0) ? materials.D : materials.black, // Down (-Y)
        (z === 2) ? materials.F : materials.black, // Front (+Z)
        (z === 0) ? materials.B : materials.black  // Back (-Z)
    ];
    return materialArray;
}

function createCubelet(x, y, z) {
    const cubeGeometry = new THREE.BoxGeometry(1, 1, 1);
    // Use logical coordinates (0,1,2) to generate materials
    const cubeMaterial = generateMaterial(x, y, z); 
    const cubelet = new THREE.Mesh(cubeGeometry, cubeMaterial);
    // Set position based on logical coordinates
    cubelet.position.set((x - 1) * 1.1, (y - 1) * 1.1, (z - 1) * 1.1);
    return cubelet;
}

export function createCube() {
    cubesArray3D = [];
    for (let x = 0; x < 3; x++) {
        cubesArray3D[x] = [];
        for (let y = 0; y < 3; y++) {
            cubesArray3D[x][y] = [];
            for (let z = 0; z < 3; z++) {
                const c = createCubelet(x, y, z);
                cubesArray3D[x][y][z] = c;
                scene.add(c);
            }
        }
    }
}

export function resetCubeObject() {
    if (cubesArray3D.length > 0) {
        cubesArray3D.forEach(layer => layer.forEach(row => row.forEach(cube => scene.remove(cube))));
    }
    cubesArray3D = [];
}

// --- Animation Functions (from your original code, for the solver animation) ---
function rotateFaceForAnimation(axis, posVal, rad) {
    const M = new THREE.Matrix4()['makeRotation' + axis.toUpperCase()](rad);
    const cubePos = new THREE.Vector3();
    for (let x = 0; x < 3; x++) {
        for (let y = 0; y < 3; y++) {
            for (let z = 0; z < 3; z++) {
                // Use logical position, not world position, for selection
                const logicalPos = (x - 1) * 1.1;
                if (Math.abs(logicalPos - posVal) < 0.1) {
                    cubesArray3D[x][y][z].applyMatrix4(M);
                }
            }
        }
    }
}
export const rotateXFace = (pos, rad) => rotateFaceForAnimation('x', pos, rad);
export const rotateYFace = (pos, rad) => rotateFaceForAnimation('y', pos, rad);
export const rotateZFace = (pos, rad) => rotateFaceForAnimation('z', pos, rad);


// --- ROBUST, STATE-FIRST, NON-ANIMATED MOVE LOGIC FOR SCRAMBLING ---
function rotateLayer(axis, slice, clockwise) {
    const tempLayer = Array(3).fill(0).map(() => Array(3).fill(null));

    if (axis === 'y') { // U, D, E moves
        for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) tempLayer[i][j] = cubesArray3D[i][slice][j];
        const rotated = rotateFaceArray(tempLayer, clockwise);
        for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) cubesArray3D[i][slice][j] = rotated[i][j];
    } else if (axis === 'x') { // R, L, M moves
        for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) tempLayer[i][j] = cubesArray3D[slice][i][j];
        const rotated = rotateFaceArray(tempLayer, clockwise);
        for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) cubesArray3D[slice][i][j] = rotated[i][j];
    } else if (axis === 'z') { // F, B, S moves
        for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) tempLayer[i][j] = cubesArray3D[i][j][slice];
        const rotated = rotateFaceArray(tempLayer, clockwise);
        for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) cubesArray3D[i][j][slice] = rotated[i][j];
    }
}

function rotateFaceArray(arr, clockwise) {
    const n = 3;
    const newArr = Array(n).fill(0).map(() => Array(n).fill(0));
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            if (clockwise) newArr[j][n - 1 - i] = arr[i][j];
            else newArr[n - 1 - j][i] = arr[i][j];
        }
    }
    return newArr;
}

function updateAllCubeletPositions() {
    for (let x = 0; x < 3; x++) {
        for (let y = 0; y < 3; y++) {
            for (let z = 0; z < 3; z++) {
                const cubelet = cubesArray3D[x][y][z];
                cubelet.position.set((x - 1) * 1.1, (y - 1) * 1.1, (z - 1) * 1.1);
                cubelet.rotation.set(0, 0, 0);
                cubelet.updateMatrix();
            }
        }
    }
}

export function applyMove(move) {
    const faceChar = move.charAt(0).toUpperCase();
    const isPrime = move.includes("'");
    const isDouble = move.includes("2");
    const turns = isDouble ? 2 : 1;

    for (let i = 0; i < turns; i++) {
        applySingleTurn(faceChar, isPrime);
    }
}

function applySingleTurn(face, isPrime) {
    const clockwise = !isPrime;
    switch (face) {
        case 'U': rotateLayer('y', 2, clockwise); break;
        case 'D': rotateLayer('y', 0, !clockwise); break;
        case 'R': rotateLayer('x', 2, clockwise); break;
        case 'L': rotateLayer('x', 0, !clockwise); break;
        case 'F': rotateLayer('z', 2, clockwise); break;
        case 'B': rotateLayer('z', 0, !clockwise); break;
    }
    updateAllCubeletPositions();
}
