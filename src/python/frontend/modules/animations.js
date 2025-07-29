// src/python/frontend/modules/animations.js

import { Keyframe, Motion } from './motion.js';
import { rotateXFace, rotateYFace, rotateZFace } from './rubik.js';

export const Faces = {
    RIGHT: 'right', LEFT: 'left', MID: 'mid',
    UP: 'up', DOWN: 'down', FRONT: 'front', BACK: 'back'
};

window.motions = {}; // Make it globally accessible for the main.js scramble setup
let activeAnimations = {};
export const duration = 0.3; // seconds

function rotateRFace(avars) { rotateXFace(avars[0], avars[1]); }
function rotateLFace(avars) { rotateXFace(avars[0], avars[1]); }
function rotateMFace(avars) { rotateXFace(avars[0], avars[1]); }
function rotateUFace(avars) { rotateYFace(avars[0], avars[1]); }
function rotateDFace(avars) { rotateYFace(avars[0], avars[1]); }
function rotateFFace(avars) { rotateZFace(avars[0], avars[1]); }
function rotateBFace(avars) { rotateZFace(avars[0], avars[1]); }

export function initMotions(clockwise = true) {
    const theta = clockwise ? -Math.PI / 2 : Math.PI / 2;
    const negTheta = -theta;

    window.motions.right = new Motion(rotateRFace);
    window.motions.left = new Motion(rotateLFace);
    window.motions.mid = new Motion(rotateMFace);
    window.motions.up = new Motion(rotateUFace);
    window.motions.down = new Motion(rotateDFace);
    window.motions.front = new Motion(rotateFFace);
    window.motions.back = new Motion(rotateBFace);

    window.motions.right.addKeyFrame(new Keyframe('beg', 0.0, [1.1, 0]));
    window.motions.right.addKeyFrame(new Keyframe('end', duration, [1.1, theta]));

    window.motions.left.addKeyFrame(new Keyframe('beg', 0.0, [-1.1, 0]));
    window.motions.left.addKeyFrame(new Keyframe('end', duration, [-1.1, negTheta]));

    window.motions.mid.addKeyFrame(new Keyframe('beg', 0.0, [0, 0]));
    window.motions.mid.addKeyFrame(new Keyframe('end', duration, [0, negTheta]));

    window.motions.up.addKeyFrame(new Keyframe('beg', 0.0, [1.1, 0]));
    window.motions.up.addKeyFrame(new Keyframe('end', duration, [1.1, theta]));

    window.motions.down.addKeyFrame(new Keyframe('beg', 0.0, [-1.1, 0]));
    window.motions.down.addKeyFrame(new Keyframe('end', duration, [-1.1, negTheta]));

    window.motions.front.addKeyFrame(new Keyframe('beg', 0.0, [1.1, 0]));
    window.motions.front.addKeyFrame(new Keyframe('end', duration, [1.1, theta]));

    window.motions.back.addKeyFrame(new Keyframe('beg', 0.0, [-1.1, 0]));
    window.motions.back.addKeyFrame(new Keyframe('end', duration, [-1.1, negTheta]));
}

function stopAnimation(face) {
    activeAnimations[face] = false;
    window.motions[face].reset();
}

export function animate(face) {
    return new Promise(resolve => {
        if (activeAnimations[face]) {
            resolve();
            return;
        }
        activeAnimations[face] = true;
        setTimeout(() => {
            stopAnimation(face);
            resolve();
        }, duration * 1000);
    });
}

export function updateAnimations(dt) {
    for (const face of Object.values(Faces)) {
        if (activeAnimations[face]) {
            let finished = window.motions[face].timestep(dt);
            if (finished) {
                stopAnimation(face);
            }
        }
    }
}
