// Fixed main application for Rubik's Cube Visualization
document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const container = document.getElementById('container');
    const statusElement = document.getElementById('status');
    const solveButton = document.getElementById('solveButton');
    const resetButton = document.getElementById('resetButton');
    
    // Cube data from server
    let cubeData = null;
    
    // Three.js setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a1a);
    
    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(5, 5, 7);
    // Make camera accessible globally for debugging
    window.camera = camera;
    
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    container.appendChild(renderer.domElement);
    
    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.1;
    controls.enableZoom = true;
    
    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(5, 10, 7);
    scene.add(directionalLight);
    
    // Initialize Rubik's cube
    const cube = new RubiksCube();
    scene.add(cube.group);
    scene.add(cube.rotatorObject);
    
    // Initialize the cube
    cube.createCube();
    
    // Load cube data from server
    async function loadCubeData() {
        try {
            statusElement.innerText = "Loading cube data...";
            
            const response = await fetch('/get_cube_data');
            if (!response.ok) {
                throw new Error(`Server returned ${response.status}`);
            }
            
            const data = await response.json();
            console.log("Loaded cube data:", data);
            
            if (!data.state || data.state.length !== 54) {
                throw new Error(`Invalid state data: ${data.state}`);
            }
            
            cubeData = data;
            
            // Apply state to the cube
            if (cube.applyState(data.state)) {
                statusElement.innerText = "Ready to solve";
                solveButton.disabled = false;
                resetButton.disabled = false;
            } else {
                throw new Error("Failed to apply cube state");
            }
        } catch (error) {
            console.error("Error loading cube data:", error);
            statusElement.innerText = `Error: ${error.message}`;
        }
    }
    
    // Event listeners
    solveButton.addEventListener('click', () => {
        if (!cubeData || !cubeData.solution) return;
        
        statusElement.innerText = "Solving...";
        solveButton.disabled = true;
        resetButton.disabled = true;
        
        // CRITICAL FIX: Add a timeout to ensure UI updates before animation starts
        setTimeout(() => {
            try {
                cube.executeSolution(cubeData.solution, () => {
                    console.log("Solution animation complete");
                    statusElement.innerText = "Solution complete!";
                    solveButton.disabled = false;
                    resetButton.disabled = false;
                });
            } catch (error) {
                console.error("Error executing solution:", error);
                statusElement.innerText = `Error: ${error.message}`;
                solveButton.disabled = false;
                resetButton.disabled = false;
            }
        }, 100);
    });
    
    resetButton.addEventListener('click', () => {
        if (!cubeData) return;
        
        try {
            console.log("Resetting cube");
            cube.createCube();
            cube.applyState(cubeData.state);
            statusElement.innerText = "Cube reset";
        } catch (error) {
            console.error("Error resetting cube:", error);
            statusElement.innerText = `Error: ${error.message}`;
        }
    });
    
    // Handle window resize
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
    
    // Animation loop
    function animate(timestamp) {
        requestAnimationFrame(animate);
        controls.update();
        
        try {
            // CRITICAL FIX: Error handling around update function
            cube.update(timestamp);
        } catch (error) {
            console.error("Error in animation update:", error);
        }
        
        renderer.render(scene, camera);
    }
    
    // Start the application
    loadCubeData();
    animate();
});