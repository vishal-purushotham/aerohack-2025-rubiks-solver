// src/python/frontend/modules/sceneManager.js

export let scene = new THREE.Scene();
let camera, renderer, controls;

export function initCanvas() {
  const canvas = document.getElementById('canvas-container');
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setClearColor(0x30322F);
  canvas.appendChild(renderer.domElement);

  camera = new THREE.PerspectiveCamera(30, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
  camera.position.set(15, 10, 10);
  camera.lookAt(0, 0, 0);
  scene.add(camera);

  controls = new THREE.OrbitControls(camera, renderer.domElement);
  
  window.addEventListener('resize', resize);
  resize();

  const light = new THREE.PointLight(0xffffff);
  light.position.set(0, 4, 2);
  scene.add(light);
  const ambientLight = new THREE.AmbientLight(0x606060);
  scene.add(ambientLight);
}

function resize() {
  const canvas = document.getElementById('canvas-container');
  renderer.setSize(canvas.clientWidth, canvas.clientHeight);
  camera.aspect = canvas.clientWidth / canvas.clientHeight;
  camera.updateProjectionMatrix();
}

export function render() {
  renderer.render(scene, camera);
}
