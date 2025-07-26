// FILE: src/python/frontend/main.js
// ACTION: Replace the entire file with this definitive, professional version.

document.addEventListener('DOMContentLoaded', () => {
    // --- Global THREE.js objects ---
    const {
        Scene, PerspectiveCamera, WebGLRenderer, Group, BoxGeometry, MeshBasicMaterial,
        Mesh, Vector3, Quaternion, PlaneGeometry, Color, AmbientLight, DirectionalLight
    } = THREE;

    // --- DOM Elements ---
    const statusElement = document.getElementById('status');
    const solveButton = document.getElementById('solveButton');
    const resetButton = document.getElementById('resetButton');

    // --- Scene Setup ---
    const scene = new Scene();
    scene.background = new Color(0x1a1a1a);
    const camera = new PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    camera.position.set(4, 4, 4);
    controls.enableDamping = true;
    controls.update();

    // --- Lighting ---
    scene.add(new AmbientLight(0xffffff, 0.8));
    const light = new DirectionalLight(0xffffff, 0.7);
    light.position.set(5, 10, 7.5);
    scene.add(light);

    // --- Cube Creation (Robust Architecture) ---
    const CUBIE_SIZE = 1;
    const CUBIE_SPACING = 0.08;
    const CUBE_GROUP = new Group();
    const CUBIES = []; // This will hold our 26 cubie meshes.

    const MATERIALS = {
        'U': new MeshBasicMaterial({ color: 0xffffff }), 'D': new MeshBasicMaterial({ color: 0xffff00 }),
        'R': new MeshBasicMaterial({ color: 0xB71C1C }), 'L': new MeshBasicMaterial({ color: 0xFF8F00 }),
        'F': new MeshBasicMaterial({ color: 0x00C853 }), 'B': new MeshBasicMaterial({ color: 0x0D47A1 }),
        'inside': new MeshBasicMaterial({ color: 0x1a1a1a })
    };

    // This data structure will hold the logical state of the cube.
    let logicalCubies = [];

    for (let x = -1; x <= 1; x++) {
        for (let y = -1; y <= 1; y++) {
            for (let z = -1; z <= 1; z++) {
                if (x === 0 && y === 0 && z === 0) continue;
                
                const geometry = new BoxGeometry(CUBIE_SIZE, CUBIE_SIZE, CUBIE_SIZE);
                // Start with all interior faces
                const meshMaterials = Array(6).fill(MATERIALS.inside);
                const cubie = new Mesh(geometry, meshMaterials);
                
                const position = new Vector3(x, y, z);
                cubie.position.copy(position).multiplyScalar(CUBIE_SIZE + CUBIE_SPACING);
                
                // Store its logical, integer-based grid position. This is the key to avoiding float errors.
                cubie.userData.gridPosition = position.clone();
                
                CUBE_GROUP.add(cubie);
                CUBIES.push(cubie);
                logicalCubies.push({ mesh: cubie, position: position.clone() });
            }
        }
    }
    scene.add(CUBE_GROUP);

    // --- State & Sticker Logic (Definitive Implementation) ---
    function applyState(stateString) {
        const faceMap = ['U', 'R', 'F', 'D', 'L', 'B'];
        const colorMap = { 'U':0, 'D':1, 'F':2, 'B':3, 'L':4, 'R':5 };
        const stickerDefs = [
            { face: 'U', normal: new Vector3(0, 1, 0), cubies: c => c.position.y === 1 },
            { face: 'D', normal: new Vector3(0, -1, 0), cubies: c => c.position.y === -1 },
            { face: 'L', normal: new Vector3(-1, 0, 0), cubies: c => c.position.x === -1 },
            { face: 'R', normal: new Vector3(1, 0, 0), cubies: c => c.position.x === 1 },
            { face: 'F', normal: new Vector3(0, 0, 1), cubies: c => c.position.z === 1 },
            { face: 'B', normal: new Vector3(0, 0, -1), cubies: c => c.position.z === -1 },
        ];

        // Reset all faces to inside material first
        CUBIES.forEach(cubie => { cubie.material = Array(6).fill(MATERIALS.inside); });
        
        let stringIndex = 0;
        for(const faceDef of stickerDefs) {
            const cubiesOnFace = logicalCubies.filter(faceDef.cubies);
            // Sort to match Kociemba's U1..U9, R1..R9 etc. string order
            cubiesOnFace.sort((a, b) => {
                if (faceDef.face === 'U' || faceDef.face === 'D') return (a.position.z - b.position.z) * 10 + (a.position.x - b.position.x);
                if (faceDef.face === 'F' || faceDef.face === 'B') return (a.position.y - b.position.y) * -10 + (a.position.x - b.position.x);
                if (faceDef.face === 'L' || faceDef.face === 'R') return (a.position.y - b.position.y) * -10 + (a.position.z - b.position.z) * -1;
                return 0;
            });

            for(const cubie of cubiesOnFace) {
                const colorChar = stateString[stringIndex++];
                const material = MATERIALS[colorChar];
                const faceIndex = cubie.mesh.geometry.groups.find(g => {
                    const plane = new THREE.Plane().setFromNormalAndCoplanarPoint(faceDef.normal, cubie.mesh.position);
                    return Math.abs(plane.normal.dot(faceDef.normal) - 1) < 0.01;
                })?.materialIndex;
                
                const normal = faceDef.normal;
                const materialIndex = (normal.y > 0.5) ? 0 : (normal.y < -0.5) ? 1 : 
                                      (normal.z > 0.5) ? 2 : (normal.z < -0.5) ? 3 :
                                      (normal.x < -0.5) ? 4 : 5;

                cubie.mesh.material[materialIndex] = material;
            }
        }
    }
    
    // --- Animation Logic (Robust Implementation) ---
    let isAnimating = false;

    async function animateMove(move) {
        if (isAnimating) return;
        isAnimating = true;
        solveButton.disabled = true;
        resetButton.disabled = true;
        statusElement.innerText = `Animating: ${move}`;

        const axis = { 'U': 'y', 'D': 'y', 'R': 'x', 'L': 'x', 'F': 'z', 'B': 'z' }[move[0]];
        const selector = {
            'U': c => c.position.y === 1, 'D': c => c.position.y === -1,
            'R': c => c.position.x === 1, 'L': c => c.position.x === -1,
            'F': c => c.position.z === 1, 'B': c => c.position.z === -1
        }[move[0]];
        
        let angle = Math.PI / 2;
        if (['D', 'L', 'B'].includes(move[0])) angle *= -1;
        if (move.includes("'")) angle *= -1;
        if (move.includes("2")) angle *= 2;

        const pivot = new Group();
        scene.add(pivot);
        const toRotate = logicalCubies.filter(selector);
        toRotate.forEach(c => pivot.add(c.mesh));

        await new Promise(resolve => {
            const start = new Quaternion();
            const end = new Quaternion().setFromAxisAngle(new Vector3(axis === 'x' ? 1:0, axis === 'y' ? 1:0, axis === 'z' ? 1:0), angle);
            let startTime = null;

            function rotate(timestamp) {
                if (!startTime) startTime = timestamp;
                const progress = Math.min((timestamp - startTime) / 250, 1);
                Quaternion.slerp(start, end, pivot.quaternion, progress);
                if (progress < 1) requestAnimationFrame(rotate);
                else resolve();
            }
            requestAnimationFrame(rotate);
        });
        
        pivot.updateMatrixWorld();
        toRotate.forEach(cubie => {
            CUBE_GROUP.add(cubie.mesh);
            cubie.mesh.applyMatrix4(pivot.matrixWorld);
            // Update logical position
            cubie.position.copy(cubie.mesh.position).round();
        });
        scene.remove(pivot);

        isAnimating = false;
        solveButton.disabled = false;
        resetButton.disabled = false;
        statusElement.innerText = 'Idle';
    }

    // --- Data Loading & UI ---
    let cubeData = {};
    async function init() {
        try {
            const response = await fetch('/get_cube_data');
            cubeData = await response.json();
            applyState(cubeData.state);
            statusElement.innerText = 'Cube loaded. Ready to animate.';
            solveButton.disabled = false;
            resetButton.disabled = false;
        } catch (e) { statusElement.innerText = 'Error loading cube data.'; console.error(e); }
    }

    solveButton.addEventListener('click', async () => {
        const solution = cubeData.solution.split(' ').filter(m => m && !m.startsWith('('));
        for (const move of solution) await animateMove(move);
    });

    resetButton.addEventListener('click', () => {
        if (isAnimating) return;
        logicalCubies.forEach(c => {
            c.mesh.position.copy(c.userData.initialPosition);
            c.mesh.quaternion.identity();
            c.position.copy(c.userData.gridPosition);
        });
        applyState(cubeData.state);
    });

    // --- Main Loop ---
    function render() {
        requestAnimationFrame(render);
        controls.update();
        renderer.render(scene, camera);
    }
    
    init();
    render();
});