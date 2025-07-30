// In src/python/frontend/modules/rubik.js (REPLACE ENTIRE FILE)

import { scene } from './sceneManager.js';

let cubesArray3D = [];

// Standard Western Color Scheme
const materials = {
    'U': new THREE.MeshBasicMaterial({ color: 0xFFFFFF, side: THREE.DoubleSide }), // White
    'D': new THREE.MeshBasicMaterial({ color: 0xFFD700, side: THREE.DoubleSide }), // Yellow
    'L': new THREE.MeshBasicMaterial({ color: 0xFF8C00, side: THREE.DoubleSide }), // Orange
    'R': new THREE.MeshBasicMaterial({ color: 0xB71C1C, side: THREE.DoubleSide }), // Red
    'F': new THREE.MeshBasicMaterial({ color: 0x009A44, side: THREE.DoubleSide }), // Green
    'B': new THREE.MeshBasicMaterial({ color: 0x003DA5, side: THREE.DoubleSide }), // Blue
    'black': new THREE.MeshBasicMaterial({ color: 0x222222, side: THREE.DoubleSide })
};

// This function correctly assigns materials to the 6 faces of a cubelet
// based on its logical position (0, 1, or 2 on each axis).
function generateMaterial(x, y, z) {
    // The center cubelet (1,1,1) is internal and all black.
    if (x === 1 && y === 1 && z === 1) {
        return materials.black;
    }

    // The order of materials for BoxGeometry is [+X, -X, +Y, -Y, +Z, -Z]
    // which corresponds to [Right, Left, Up, Down, Front, Back]
    const materialArray = [
        (x === 2) ? materials.R : materials.black, // Right face is at logical x=2
        (x === 0) ? materials.L : materials.black, // Left face is at logical x=0
        (y === 2) ? materials.U : materials.black, // Up face is at logical y=2
        (y === 0) ? materials.D : materials.black, // Down face is at logical y=0
        (z === 2) ? materials.F : materials.black, // Front face is at logical z=2
        (z === 0) ? materials.B : materials.black  // Back face is at logical z=0
    ];
    return materialArray;
}

function createCubelet(x, y, z) {
    const cubeGeometry = new THREE.BoxGeometry(1, 1, 1);
    const cubeMaterial = generateMaterial(x, y, z);
    const cubelet = new THREE.Mesh(cubeGeometry, cubeMaterial);
    // Position the cubelet in 3D space based on its logical coordinates
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

// Dummy functions to prevent crashes from other files calling them.
export function applyMove(move) { 
    console.log(`DUMMY: applyMove(${move})`);
}
export const rotateXFace = (pos, rad) => {};
export const rotateYFace = (pos, rad) => {};
export const rotateZFace = (pos, rad) => {};
