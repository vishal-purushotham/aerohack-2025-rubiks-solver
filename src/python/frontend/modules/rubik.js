export default class RubiksCube {
    constructor(order = 3, size = 1, debug = false) {
        this.cubeOrder = order;
        this.size = size;
        this.debug = debug;
        this.group = new THREE.Group();
        this.cubies = [];

        // Animation state
        this.isRotating = false;
        this.completeCallback = null;

        // Colors mapping
        this.colors = {
            U: 0xffffff, // White
            D: 0xffff00, // Yellow
            L: 0x009a44, // Green
            R: 0x003da5, // Blue
            F: 0xba0c2f, // Red
            B: 0xfe5000, // Orange
        };
        
        this.rotatorObject = new THREE.Object3D();
        this.activeCubies = [];
        this.rotateAxisLocal = null;
        this.targetAngle = 0;
        this.rotatedAngle = 0;
        this.lastTick = 0;

        this.createCube();
        this.group.add(this.rotatorObject);
    }

    // Get the main group for adding to a scene
    get object() {
        return this.group;
    }

    // Create the Rubik's Cube from cubies
    createCube() {
        this.group.rotation.x = -Math.PI / 6;
        this.group.rotation.y = -Math.PI / 4;

        const offset = (this.cubeOrder - 1) / 2;

        for (let x = 0; x < this.cubeOrder; x++) {
            for (let y = 0; y < this.cubeOrder; y++) {
                for (let z = 0; z < this.cubeOrder; z++) {
                    // Skip the core cubie
                    if (x > 0 && x < this.cubeOrder - 1 && y > 0 && y < this.cubeOrder - 1 && z > 0 && z < this.cubeOrder - 1) {
                        continue;
                    }

                    const cubie = this.createCubie(x - offset, y - offset, z - offset);
                    this.cubies.push(cubie);
                    this.group.add(cubie);
                }
            }
        }
    }

    // Create a single cubie with its facelets
    createCubie(x, y, z) {
        const cubie = new THREE.Group();
        cubie.position.set(x, y, z);

        const faceletSize = 0.9;
        const faceletGeo = new THREE.PlaneGeometry(faceletSize, faceletSize);

        const faces = [
            { dir: new THREE.Vector3(0, 1, 0), color: this.colors.U, name: 'U' }, // Up
            { dir: new THREE.Vector3(0, -1, 0), color: this.colors.D, name: 'D' }, // Down
            { dir: new THREE.Vector3(-1, 0, 0), color: this.colors.L, name: 'L' }, // Left
            { dir: new THREE.Vector3(1, 0, 0), color: this.colors.R, name: 'R' }, // Right
            { dir: new THREE.Vector3(0, 0, 1), color: this.colors.F, name: 'F' }, // Front
            { dir: new THREE.Vector3(0, 0, -1), color: this.colors.B, name: 'B' }, // Back
        ];

        const offset = (this.cubeOrder - 1) / 2;

        faces.forEach(face => {
            // Check if this cubie is on the surface of the specified face
            if (Math.abs(cubie.position.dot(face.dir) - offset) < 0.1) {
                const faceletMat = new THREE.MeshBasicMaterial({ color: face.color, side: THREE.DoubleSide });
                const facelet = new THREE.Mesh(faceletGeo, faceletMat);

                facelet.position.copy(face.dir).multiplyScalar(0.5);
                facelet.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), face.dir);
                facelet.userData = { face: face.name };
                cubie.add(facelet);
            }
        });

        return cubie;
    }

    // Apply a cube state string to the cubie-based visualization
    applyState(stateString) {
        if (!stateString || stateString.length !== 54) {
            console.error("Invalid cube state string:", stateString);
            return false;
        }

        console.log("Applying state to cubies:", stateString);

        const faces = {
            U: stateString.substring(0, 9).split(''),
            R: stateString.substring(9, 18).split(''),
            F: stateString.substring(18, 27).split(''),
            D: stateString.substring(27, 36).split(''),
            L: stateString.substring(36, 45).split(''),
            B: stateString.substring(45, 54).split(''),
        };

        const faceletsByFace = this.getFaceletsByFace();

        for (const face in faces) {
            const facelets = faceletsByFace[face];
            const colors = faces[face];

            if (facelets.length !== 9) {
                console.error(`Face ${face} has ${facelets.length} facelets, expected 9.`);
                continue;
            }

            for (let i = 0; i < 9; i++) {
                const colorChar = colors[i];
                if (this.colors[colorChar]) {
                    facelets[i].material.color.setHex(this.colors[colorChar]);
                } else {
                    console.error(`Invalid color character '${colorChar}' for face ${face}`);
                }
            }
        }

        return true;
    }

    // Helper to get and sort facelets for each face
    getFaceletsByFace() {
        const facelets = { U: [], R: [], F: [], D: [], L: [], B: [] };

        this.cubies.forEach(cubie => {
            cubie.children.forEach(facelet => {
                facelets[facelet.userData.face].push(facelet);
            });
        });

        // Sort the facelets for each face to match Kociemba's order
        for (const face in facelets) {
            facelets[face].sort((a, b) => {
                const posA = a.parent.position;
                const posB = b.parent.position;

                switch (face) {
                    case 'U': return posA.z - posB.z || posA.x - posB.x;
                    case 'D': return -posA.z - -posB.z || posA.x - posB.x;
                    case 'R': return -posA.y - -posB.y || posA.z - posB.z;
                    case 'L': return -posA.y - -posB.y || -posA.z - -posB.z;
                    case 'F': return -posA.y - -posB.y || posA.x - posB.x;
                    case 'B': return -posA.y - -posB.y || -posA.x - -posB.x;
                    default: return 0;
                }
            });
        }

        return facelets;
    }

    // Perform a face rotation on cubies
    rotateFace(face, direction, callback) {
        if (this.isRotating) {
            console.log("Already rotating, skipping");
            return false;
        }

        console.log(`Rotating face ${face} in direction ${direction}`);
        this.isRotating = true;
        this.completeCallback = callback || null;

        const axis = this.getFaceNormal(face);
        const layer = (this.cubeOrder - 1) / 2;

        this.activeCubies = this.cubies.filter(cubie => {
            // Select cubies in the correct layer
            const pos = cubie.position;
            if (Math.abs(pos.x - layer * axis.x) < 0.1 && axis.x !== 0) return true;
            if (Math.abs(pos.y - layer * axis.y) < 0.1 && axis.y !== 0) return true;
            if (Math.abs(pos.z - layer * axis.z) < 0.1 && axis.z !== 0) return true;
            return false;
        });

        if (this.activeCubies.length !== 9) {
            console.error(`Expected 9 cubies for rotation, found ${this.activeCubies.length}`);
        }

        this.rotatorObject.rotation.set(0, 0, 0);
        this.rotatorObject.updateMatrixWorld();

        this.activeCubies.forEach(cubie => {
            this.group.remove(cubie);
            this.rotatorObject.add(cubie);
        });

        this.rotateAxisLocal = axis;
        this.targetAngle = (Math.PI / 2) * direction;
        this.rotatedAngle = 0;
        this.lastTick = 0;

        return true;
    }

    // Animate the rotation
    updateRotation() {
        if (!this.isRotating) return;

        const now = Date.now();
        const delta = (this.lastTick > 0) ? (now - this.lastTick) / 1000 : 0;
        this.lastTick = now;

        const speed = 3; // Radians per second
        let angleToRotate = delta * speed;

        if (this.rotatedAngle + angleToRotate >= Math.abs(this.targetAngle)) {
            angleToRotate = Math.abs(this.targetAngle) - this.rotatedAngle;
            this.rotatedAngle = Math.abs(this.targetAngle);
        } else {
            this.rotatedAngle += angleToRotate;
        }

        const rotationDirection = Math.sign(this.targetAngle);
        this.rotatorObject.rotateOnWorldAxis(this.rotateAxisLocal, angleToRotate * rotationDirection);

        if (this.rotatedAngle >= Math.abs(this.targetAngle)) {
            this.finishRotation();
        }
    }

    // Get the normal vector for a given face name
    getFaceNormal(face) {
        switch (face) {
            case 'U': return new THREE.Vector3(0, 1, 0);
            case 'D': return new THREE.Vector3(0, -1, 0);
            case 'L': return new THREE.Vector3(-1, 0, 0);
            case 'R': return new THREE.Vector3(1, 0, 0);
            case 'F': return new THREE.Vector3(0, 0, 1);
            case 'B': return new THREE.Vector3(0, 0, -1);
            default: return new THREE.Vector3(0, 0, 0);
        }
    }

    // Finish the rotation and update cubie states
    finishRotation() {
        console.log("Finishing rotation");

        this.rotatorObject.updateMatrixWorld();

        // Update cubie positions and rotations logically
        this.activeCubies.forEach(cubie => {
            const newMatrix = cubie.matrixWorld.clone();
            this.rotatorObject.remove(cubie);
            this.group.add(cubie);
            cubie.applyMatrix4(newMatrix);

            // Round positions to snap them into place
            cubie.position.round();
            cubie.rotation.setFromRotationMatrix(cubie.matrix);
        });

        try {
            // Reset rotation state
            this.isRotating = false;
            this.activeCubies = [];
            this.rotateAxisLocal = null;
            this.targetAngle = 0;
            this.rotatedAngle = 0;
            this.lastTick = 0;

            if (this.completeCallback) {
                this.completeCallback();
                this.completeCallback = null;
            }
        } catch (e) {
            console.error("Error in finishRotation callback:", e);
        }
    }
}
