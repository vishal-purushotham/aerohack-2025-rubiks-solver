// Import the scene here to facilitate cube creation and modification
// Directly modifying the scene during cube creation improves performance
import { scene } from "./sceneManager.js";

///////////////////////////////////////////////////////////////////////////////////////////
//  MATERIALS
///////////////////////////////////////////////////////////////////////////////////////////

let blackMaterial = new THREE.MeshBasicMaterial({ color: 0x000000 });
let blueMaterial = new THREE.MeshBasicMaterial( { color: 0x003DA5 } );
let greenMaterial = new THREE.MeshBasicMaterial( { color: 0x009A44 } );
let whiteMaterial = new THREE.MeshBasicMaterial( { color: 0xFFFFFF } );
let yellowMaterial = new THREE.MeshBasicMaterial( { color: 0xFFD700 } );
let redMaterial = new THREE.MeshBasicMaterial( { color: 0xBA0C2F } );
let orangeMaterial = new THREE.MeshBasicMaterial( { color: 0xFE5000 } );

///////////////////////////////////////////////////////////////////////////////////////////
//  OBJECTS
///////////////////////////////////////////////////////////////////////////////////////////

function createCubelet(x, y, z, cubeState) {
  let cubeGeometry = new THREE.BoxGeometry(1, 1, 1);
  let cubeMaterial = generateMaterial(x, y, z, cubeState);
  let cubelet = new THREE.Mesh(cubeGeometry, cubeMaterial);
  cubelet.position.set(x, y, z);
  return cubelet;
}

const colorMap = {
    'U': whiteMaterial,
    'R': blueMaterial,
    'F': redMaterial,
    'D': yellowMaterial,
    'L': greenMaterial,
    'B': orangeMaterial,
};

function generateMaterial(x, y, z, cubeState) {
    if (x === 0 && y === 0 && z === 0) return blackMaterial; // Center piece is black

    const materials = Array(6).fill(blackMaterial);
    const stateOrder = 'URFDLB';

    // Map coordinates to 0, 1, 2 indices
    const i = Math.round((x + 1.1) / 1.1);
    const j = Math.round((y + 1.1) / 1.1);
    const k = Math.round((z + 1.1) / 1.1);

    if (cubeState) {
        const faceMap = {
            'U': (2 - k) * 3 + i,       // Up face (y = 1.1)
            'R': (2 - j) * 3 + (2-k),   // Right face (x = 1.1)
            'F': (2 - j) * 3 + i,       // Front face (z = 1.1)
            'D': k * 3 + i,             // Down face (y = -1.1)
            'L': (2 - j) * 3 + k,       // Left face (x = -1.1)
            'B': (2 - j) * 3 + (2-i),   // Back face (z = -1.1)
        };

        // Order of materials for THREE.BoxGeometry: R, L, U, D, F, B (x+, x-, y+, y-, z+, z-)
        if (Math.abs(x - 1.1) < 0.1)  materials[0] = colorMap[cubeState[stateOrder.indexOf('R') * 9 + faceMap['R']]];
        if (Math.abs(x + 1.1) < 0.1)  materials[1] = colorMap[cubeState[stateOrder.indexOf('L') * 9 + faceMap['L']]];
        if (Math.abs(y - 1.1) < 0.1)  materials[2] = colorMap[cubeState[stateOrder.indexOf('U') * 9 + faceMap['U']]];
        if (Math.abs(y + 1.1) < 0.1)  materials[3] = colorMap[cubeState[stateOrder.indexOf('D') * 9 + faceMap['D']]];
        if (Math.abs(z - 1.1) < 0.1)  materials[4] = colorMap[cubeState[stateOrder.indexOf('F') * 9 + faceMap['F']]];
        if (Math.abs(z + 1.1) < 0.1)  materials[5] = colorMap[cubeState[stateOrder.indexOf('B') * 9 + faceMap['B']]];

    } else {
        // Default solved state materials
        if (Math.abs(x - 1.1) < 0.1) materials[0] = blueMaterial;
        if (Math.abs(x + 1.1) < 0.1) materials[1] = greenMaterial;
        if (Math.abs(y - 1.1) < 0.1) materials[2] = whiteMaterial;
        if (Math.abs(y + 1.1) < 0.1) materials[3] = yellowMaterial;
        if (Math.abs(z - 1.1) < 0.1) materials[4] = redMaterial;
        if (Math.abs(z + 1.1) < 0.1) materials[5] = orangeMaterial;
    }
    return materials;
}

export let cubesArray3D = [];
export function createCube(cubeState = null) {
  cubesArray3D = [];
  for (let x = -1.1; x <= 1.1; x += 1.1) {
    let why = [];
    for (let y = -1.1; y <= 1.1; y += 1.1) {
      let zed = [];
      for (let z = -1.1; z <= 1.1; z += 1.1) {
        const c = createCubelet(x, y, z, cubeState);
        zed.push(c);
        scene.add(c);
      }
      why.push(zed);
    }
    cubesArray3D.push(why);
  }
}

export function resetCubeObject(cubeState = null) {
  cubesArray3D.forEach(layer => {
    layer.forEach(row => {
      row.forEach(cube => {
        scene.remove(cube);
      });
    });
  });
  createCube(cubeState);
}

///////////////////////////////////////////////////////////////////////////////////////
// FACE ROTATION HELPER FUNCTIONS (shared rotation behaviour for each axis)
///////////////////////////////////////////////////////////////////////////////////////

// special rounding helper function, rounds value to -1.1, 0, 1.1
function round(v) {
  var distToZero = Math.abs(v);
  var distToPos = Math.abs(1.1-v);
  var distToNeg = Math.abs(-1.1-v);
  if (distToZero < distToNeg && distToZero < distToPos) {
    return 0;
  }
  if (distToNeg < distToZero && distToNeg < distToPos) {
    return -1.1;
  } 
  return 1.1; // closer to 1.1 case
}

// rotate x faces (R,L,M)
export function rotateXFace(xpos, rad) {
  let M = new THREE.Matrix4();
  M.makeRotationX(rad);
  let cubePos = new THREE.Vector3();
  // perform rotation
  for (let x = 0; x < 3; x++) {
      for (let y = 0; y < 3; y++) {
          for (let z = 0; z < 3; z++) {
              if (round(cubesArray3D[x][y][z].getWorldPosition(cubePos).x) == xpos) {
                  cubesArray3D[x][y][z].matrixAutoUpdate = false;
                  cubesArray3D[x][y][z].matrix.premultiply(M);
                  cubesArray3D[x][y][z].updateMatrixWorld();
              }
          }
      }
  }
}
// rotate y faces (U, D)
export function rotateYFace(ypos, rad) {
  let M = new THREE.Matrix4();
  M.makeRotationY(rad);
  let cubePos = new THREE.Vector3();
  // perform rotation
  for (let x = 0; x < 3; x++) {
      for (let y = 0; y < 3; y++) {
          for (let z = 0; z < 3; z++) {
              if (round(cubesArray3D[x][y][z].getWorldPosition(cubePos).y) == ypos) {
                  cubesArray3D[x][y][z].matrixAutoUpdate = false;
                  cubesArray3D[x][y][z].matrix.premultiply(M);
                  cubesArray3D[x][y][z].updateMatrixWorld();
              }
          }
      }
  }
}
// rotate z faces (F, B)
export function rotateZFace(zpos, rad) {
  let M = new THREE.Matrix4();
  M.makeRotationZ(rad);
  let cubePos = new THREE.Vector3();
  // perform rotation
  for (let x = 0; x < 3; x++) {
      for (let y = 0; y < 3; y++) {
          for (let z = 0; z < 3; z++) {
              if (round(cubesArray3D[x][y][z].getWorldPosition(cubePos).z) == zpos) {
                  cubesArray3D[x][y][z].matrixAutoUpdate = false;
                  cubesArray3D[x][y][z].matrix.premultiply(M);
                  cubesArray3D[x][y][z].updateMatrixWorld();
              }
          }
      }
  }
}
