// Improved Rubik's cube implementation with fixed colors and animation
class RubiksCube {
    constructor() {
        this.cubeOrder = 3; // Fixed 3x3 cube
        this.elementSize = 1;
        this.elements = [];
        this.rotateSpeed = 1.0; // Increased speed
        this.isRotating = false;
        this.group = new THREE.Group();

        // Define standard colors for the cube faces
        // CRITICAL FIX: Ensure these colors exactly match Rubik's standard colors
        this.colors = {
            'U': 0xFFFFFF, // White (Up)
            'D': 0xFFFF00, // Yellow (Down)
            'R': 0xB71C1C, // Red (Right) - using more precise red
            'L': 0xFF8800, // Orange (Left)
            'F': 0x00C853, // Green (Front) - using more precise green
            'B': 0x0045AD, // Blue (Back) - using more precise blue
            'X': 0x000000  // Black (for debugging)
        };
        
        this.rotatorObject = new THREE.Object3D();
        this.activeSquares = [];
        this.rotateAxisLocal = null;
        this.targetAngle = 0;
        this.rotatedAngle = 0;
        this.lastTick = 0;
        this.completeCallback = null;
        
        // Debug mode
        this.debug = false;
    }

    // Create the initial cube configuration
    createCube() {
        console.log("Creating cube...");
        this.group.clear();
        this.elements = [];
        
        // Create elements for all six faces
        this.createElements();
        
        // Create visual squares from the elements data
        for (let i = 0; i < this.elements.length; i++) {
            const square = this.createSquare(this.elements[i]);
            this.group.add(square);
        }
        
        // Set initial rotation
        this.group.rotation.x = Math.PI * 0.25;
        this.group.rotation.y = Math.PI * 0.25;
        
        return this.group;
    }

    // Create the data structure for all square elements
    createElements() {
        this.elements = [];
        const border = (this.cubeOrder * this.elementSize) / 2 - 0.5;

        // Top (U) and bottom (D) faces
        for (let x = -border; x <= border; x++) {
            for (let z = -border; z <= border; z++) {
                this.elements.push({
                    color: this.colors.U,
                    pos: new THREE.Vector3(x, border + this.elementSize * 0.5, z),
                    normal: new THREE.Vector3(0, 1, 0),
                    face: 'U'
                });

                this.elements.push({
                    color: this.colors.D,
                    pos: new THREE.Vector3(x, -border - this.elementSize * 0.5, z),
                    normal: new THREE.Vector3(0, -1, 0),
                    face: 'D'
                });
            }
        }

        // Left (L) and right (R) faces
        for (let y = -border; y <= border; y++) {
            for (let z = -border; z <= border; z++) {
                this.elements.push({
                    color: this.colors.L,
                    pos: new THREE.Vector3(-border - this.elementSize * 0.5, y, z),
                    normal: new THREE.Vector3(-1, 0, 0),
                    face: 'L'
                });

                this.elements.push({
                    color: this.colors.R,
                    pos: new THREE.Vector3(border + this.elementSize * 0.5, y, z),
                    normal: new THREE.Vector3(1, 0, 0),
                    face: 'R'
                });
            }
        }

        // Front (F) and back (B) faces
        for (let x = -border; x <= border; x++) {
            for (let y = -border; y <= border; y++) {
                this.elements.push({
                    color: this.colors.F,
                    pos: new THREE.Vector3(x, y, border + this.elementSize * 0.5),
                    normal: new THREE.Vector3(0, 0, 1),
                    face: 'F'
                });

                this.elements.push({
                    color: this.colors.B,
                    pos: new THREE.Vector3(x, y, -border - this.elementSize * 0.5),
                    normal: new THREE.Vector3(0, 0, -1),
                    face: 'B'
                });
            }
        }
    }

    // Create a visual square element from data
    createSquare(element) {
        // Create a square shape with rounded corners
        const squareShape = new THREE.Shape();
        const x = 0, y = 0;
        
        // Create the shape with rounded corners
        squareShape.moveTo(x - 0.4, y + 0.5);
        squareShape.lineTo(x + 0.4, y + 0.5);
        squareShape.bezierCurveTo(x + 0.5, y + 0.5, x + 0.5, y + 0.5, x + 0.5, y + 0.4);
        squareShape.lineTo(x + 0.5, y - 0.4);
        squareShape.bezierCurveTo(x + 0.5, y - 0.5, x + 0.5, y - 0.5, x + 0.4, y - 0.5);
        squareShape.lineTo(x - 0.4, y - 0.5);
        squareShape.bezierCurveTo(x - 0.5, y - 0.5, x - 0.5, y - 0.5, x - 0.5, y - 0.4);
        squareShape.lineTo(x - 0.5, y + 0.4);
        squareShape.bezierCurveTo(x - 0.5, y + 0.5, x - 0.5, y + 0.5, x - 0.4, y + 0.5);

        // Create geometry and material
        const geometry = new THREE.ShapeGeometry(squareShape);
        const material = new THREE.MeshBasicMaterial({ color: element.color });
        const mesh = new THREE.Mesh(geometry, material);
        mesh.scale.set(0.9, 0.9, 0.9);

        // Create the square object
        const square = new THREE.Object3D();
        square.element = element; // Store reference to element data
        square.add(mesh);

        // Create black border
        const borderMaterial = new THREE.MeshBasicMaterial({
            color: 0x000000,
            side: THREE.DoubleSide
        });
        const border = new THREE.Mesh(geometry, borderMaterial);
        border.position.z = -0.01;
        square.add(border);

        // Position and orient the square
        square.position.copy(element.pos);
        square.lookAt(element.pos.clone().add(element.normal));

        return square;
    }

    // Apply a cube state string to the visualization
    applyState(stateString) {
        if (!stateString || stateString.length !== 54) {
            console.error("Invalid cube state string:", stateString);
            return false;
        }

        console.log("Applying state:", stateString);

        // Parse the 6 faces from the state string (URFDLB order)
        const faces = {
            U: stateString.substring(0, 9).split(''),
            R: stateString.substring(9, 18).split(''),
            F: stateString.substring(18, 27).split(''),
            D: stateString.substring(27, 36).split(''),
            L: stateString.substring(36, 45).split(''),
            B: stateString.substring(45, 54).split('')
        };

        // Debug log
        Object.keys(faces).forEach(face => {
            console.log(`${face} face: ${faces[face].join('')}`);
        });

        // Get all squares by face
        const faceSquares = {
            U: [], R: [], F: [], D: [], L: [], B: []
        };

        // Group squares by face
        this.group.children.forEach(square => {
            const face = square.element.face;
            faceSquares[face].push(square);
        });

        // Sort squares within each face in the correct reading order
        for (const face in faceSquares) {
            this.sortFaceSquares(faceSquares[face], face);
        }

        // Apply colors to each face
        for (const face in faces) {
            const squares = faceSquares[face];
            const colors = faces[face];

            if (squares.length !== 9) {
                console.error(`Expected 9 squares for face ${face}, but found ${squares.length}`);
            }

            for (let i = 0; i < 9; i++) {
                const colorChar = colors[i];
                if (!this.colors[colorChar]) {
                    console.error(`Unknown color character: ${colorChar}`);
                    continue;
                }
                squares[i].children[0].material.color.setHex(this.colors[colorChar]);
                
                if (this.debug) {
                    // For debugging - add index to help visualize order
                    const text = document.createElement('div');
                    text.textContent = i;
                    text.style.position = 'absolute';
                    text.style.color = 'black';
                    text.style.fontSize = '20px';
                    document.body.appendChild(text);
                    
                    // Project the position to screen
                    const pos = squares[i].position.clone();
                    pos.project(window.camera);
                    text.style.left = (pos.x * window.innerWidth/2 + window.innerWidth/2) + 'px';
                    text.style.top = (-pos.y * window.innerHeight/2 + window.innerHeight/2) + 'px';
                }
            }
        }

        return true;
    }

    // Sort squares within a face in the standard reading order
    sortFaceSquares(squares, face) {
        squares.sort((a, b) => {
            const posA = a.element.pos;
            const posB = b.element.pos;
            
            switch (face) {
                case 'U': // Top view, sort back to front, left to right
                    return posA.z !== posB.z ? posA.z - posB.z : posA.x - posB.x;
                    
                case 'D': // Bottom view, sort front to back, left to right
                    return posA.z !== posB.z ? posB.z - posA.z : posA.x - posB.x;
                    
                case 'F': // Front view, sort top to bottom, left to right
                    return posA.y !== posB.y ? posB.y - posA.y : posA.x - posB.x;
                    
                case 'B': // Back view, sort top to bottom, right to left
                    return posA.y !== posB.y ? posB.y - posA.y : posB.x - posA.x;
                    
                case 'L': // Left view, sort top to bottom, back to front
                    return posA.y !== posB.y ? posB.y - posA.y : posB.z - posA.z;
                    
                case 'R': // Right view, sort top to bottom, front to back
                    return posA.y !== posB.y ? posB.y - posA.y : posA.z - posB.z;
                    
                default:
                    return 0;
            }
        });
    }

    // Perform a face rotation
    rotateFace(face, direction, callback) {
        if (this.isRotating) {
            console.log("Already rotating, skipping");
            return false;
        }
        
        console.log(`Rotating face ${face} direction ${direction}`);
        
        this.isRotating = true;
        this.completeCallback = callback || null;
        
        // Determine which face to rotate and the axis of rotation
        const normalVector = this.getFaceNormal(face);
        const rotateSquares = this.group.children.filter(square => {
            return square.element.normal.equals(normalVector);
        });
        
        if (rotateSquares.length !== 9) {
            console.error(`Expected 9 squares for rotation, found ${rotateSquares.length}`);
        }
        
        this.activeSquares = rotateSquares;
        this.rotateAxisLocal = normalVector.clone();
        this.targetAngle = (Math.PI / 2) * direction;
        this.rotatedAngle = 0;
        this.lastTick = 0;

        // Move squares to rotation object
        rotateSquares.forEach(square => {
            // Get world position before removing
            const worldPos = new THREE.Vector3();
            square.getWorldPosition(worldPos);
            
            // Remove from group and add to rotator
            this.group.remove(square);
            this.rotatorObject.add(square);
            
            // Preserve original world position
            square.position.copy(worldPos);
        });
        
        return true;
    }

    // Get the normal vector for a given face
    getFaceNormal(face) {
        switch (face) {
            case 'U': return new THREE.Vector3(0, 1, 0);
            case 'D': return new THREE.Vector3(0, -1, 0);
            case 'R': return new THREE.Vector3(1, 0, 0);
            case 'L': return new THREE.Vector3(-1, 0, 0);
            case 'F': return new THREE.Vector3(0, 0, 1);
            case 'B': return new THREE.Vector3(0, 0, -1);
            default: return new THREE.Vector3(0, 1, 0);
        }
    }

    // Animation update for rotations
    update(timestamp) {
        if (!this.isRotating) return;

        if (!this.lastTick) {
            this.lastTick = timestamp;
            return;
        }
        
        const delta = timestamp - this.lastTick;
        this.lastTick = timestamp;
        
        // Calculate rotation for this frame
        const rotateAmount = Math.min(
            this.rotateSpeed * delta / 1000 * Math.PI, 
            Math.abs(this.targetAngle) - Math.abs(this.rotatedAngle)
        );
        
        if (rotateAmount > 0) {
            const direction = this.targetAngle > 0 ? 1 : -1;
            const angle = rotateAmount * direction;
            
            // Apply rotation
            const rotationMatrix = new THREE.Matrix4().makeRotationAxis(this.rotateAxisLocal, angle);
            this.rotatorObject.applyMatrix4(rotationMatrix);
            
            this.rotatedAngle += rotateAmount * direction;
            
            // Check if rotation is complete
            if (Math.abs(this.rotatedAngle) >= Math.abs(this.targetAngle) - 0.001) {
                this.finishRotation();
            }
        }
    }

    // Finish the rotation and update cube state
    finishRotation() {
        console.log("Finishing rotation");
        
        try {
            // Update positions and normals of rotated elements
            this.activeSquares.forEach(square => {
                const normal = square.element.normal.clone();
                const position = square.element.pos.clone();
                
                // Apply the rotation to normal and position
                normal.applyAxisAngle(this.rotateAxisLocal, this.targetAngle);
                position.applyAxisAngle(this.rotateAxisLocal, this.targetAngle);
                
                // Round positions to avoid floating point issues
                position.x = Math.round(position.x * 100) / 100;
                position.y = Math.round(position.y * 100) / 100;
                position.z = Math.round(position.z * 100) / 100;
                
                // Update element data
                square.element.normal = normal;
                square.element.pos = position;
                
                // Move back to main group with world position preserved
                const worldPos = new THREE.Vector3();
                square.getWorldPosition(worldPos);
                
                this.rotatorObject.remove(square);
                this.group.add(square);
                
                // Update square position relative to the group
                const inverseMatrix = new THREE.Matrix4().copy(this.group.matrixWorld).invert();
                worldPos.applyMatrix4(inverseMatrix);
                square.position.copy(worldPos);
            });
            
            // Reset rotation state
            this.isRotating = false;
            this.activeSquares = [];
            this.rotateAxisLocal = null;
            this.targetAngle = 0;
            this.rotatedAngle = 0;
            this.lastTick = 0;
            
            // Call completion callback if provided
            if (this.completeCallback) {
                const callback = this.completeCallback;
                this.completeCallback = null;
                
                // Use setTimeout to ensure clean call stack
                setTimeout(() => {
                    callback();
                }, 0);
            }
        } catch (error) {
            console.error("Error during rotation completion:", error);
            // Reset state even on error
            this.isRotating = false;
            this.activeSquares = [];
            this.rotateAxisLocal = null;
            this.targetAngle = 0;
            this.rotatedAngle = 0;
            this.lastTick = 0;
            
            if (this.completeCallback) {
                const callback = this.completeCallback;
                this.completeCallback = null;
                setTimeout(() => {
                    callback();
                }, 0);
            }
        }
    }

    // Parse a move (e.g., "R", "U'", "F2") and execute it
    executeMove(moveStr, callback) {
        const face = moveStr[0];
        let direction = moveStr.includes("'") ? -1 : 1;
        const count = moveStr.includes("2") ? 2 : 1;
        
        console.log(`Executing move: ${moveStr} (${face}, ${direction}, ${count})`);
        
        // Execute the move
        this.executeMoveSequence([{ face, direction, count }], callback);
    }

    // Execute a sequence of moves
    executeMoveSequence(moves, finalCallback) {
        if (!moves.length) {
            console.log("Move sequence complete");
            if (finalCallback) finalCallback();
            return;
        }
        
        const move = moves[0];
        const remainingMoves = moves.slice(1);
        let completedCount = 0;
        
        const executeNextRotation = () => {
            completedCount++;
            console.log(`Completed ${completedCount} of ${move.count} for move ${move.face}`);
            
            if (completedCount < move.count) {
                // Continue with another rotation for this move
                if (!this.rotateFace(move.face, move.direction, executeNextRotation)) {
                    console.error("Failed to start rotation, skipping to next");
                    if (remainingMoves.length > 0) {
                        this.executeMoveSequence(remainingMoves, finalCallback);
                    } else {
                        if (finalCallback) finalCallback();
                    }
                }
            } else if (remainingMoves.length > 0) {
                // Continue with next move
                this.executeMoveSequence(remainingMoves, finalCallback);
            } else {
                // All moves complete
                console.log("All moves complete");
                if (finalCallback) finalCallback();
            }
        };
        
        // Start the first rotation
        if (!this.rotateFace(move.face, move.direction, executeNextRotation)) {
            console.error("Failed to start rotation sequence");
            if (finalCallback) finalCallback();
        }
    }

    // Execute a solution string (e.g. "R U R' U'")
    executeSolution(solutionString, callback) {
        if (!solutionString) {
            console.log("No solution provided");
            if (callback) callback();
            return;
        }
        
        console.log(`Executing solution: ${solutionString}`);
        
        const moves = solutionString.split(' ')
            .filter(move => move.length > 0)
            .map(moveStr => {
                const face = moveStr[0];
                let direction = moveStr.includes("'") ? -1 : 1;
                const count = moveStr.includes("2") ? 2 : 1;
                return { face, direction, count };
            });
        
        console.log(`Parsed ${moves.length} moves`);
        this.executeMoveSequence(moves, callback);
    }
}