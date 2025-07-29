// src/python/frontend/modules/motion.js

class Keyframe {
    constructor(name, time, avars) {
        this.name = name;
        this.time = time;
        this.avars = avars;
    }
}

class Motion {
    constructor(setMatricesFunc) {
        this.keyFrameArray = [];
        this.maxTime = 0.0;
        this.currTime = 0.0;
        this.updateMatrices = setMatricesFunc;
    }
    reset() {
        this.currTime = 0.0;
    }
    addKeyFrame(keyframe) {
        this.keyFrameArray.push(keyframe);
        if (keyframe.time > this.maxTime)
            this.maxTime = keyframe.time;
    }
    timestep(dt) {
        this.currTime += dt;
        if (this.currTime > this.maxTime) {
            this.currTime = 0;
            return 1; // finished
        }
        let avars = this.getAvars();
        this.updateMatrices(avars);
        return 0; // stepped
    }
    getAvars() {
        let i = 1;
        while (this.currTime > this.keyFrameArray[i].time) i++;
        let avars = [];
        for (let n = 0; n < this.keyFrameArray[i - 1].avars.length; n++) {
            let y0 = this.keyFrameArray[i - 1].avars[n];
            let y1 = this.keyFrameArray[i].avars[n];
            let x0 = this.keyFrameArray[i - 1].time;
            let x1 = this.keyFrameArray[i].time;
            let x = this.currTime;
            let y = y0 + (y1 - y0) * (x - x0) / (x1 - x0);
            avars.push(y);
        }
        return avars;
    }
}

export { Keyframe, Motion };
