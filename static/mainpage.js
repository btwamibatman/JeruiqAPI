import * as THREE from "three";
import { OrbitControls } from "OrbitControls";
import { EffectComposer } from "EffectComposer";
import { RenderPass } from "RenderPass";
import { ShaderPass } from "ShaderPass";

import getStarfield from "./src/getStarfield.js";
import { getFresnelMat } from "./src/getFresnelMat.js";

const w = window.innerWidth;
const h = window.innerHeight;

const scene = new THREE.Scene(); // THREE is already in the global scope
const camera = new THREE.PerspectiveCamera(75, w / h, 0.01, 1000);

camera.position.z = 2.1;

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(w, h);

document.body.appendChild(renderer.domElement);
// THREE.ColorManagement.enabled = true;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.outputColorSpace = THREE.LinearSRGBColorSpace;

const earthGroup = new THREE.Group();

earthGroup.rotation.z = -23.4 * Math.PI / 180;
scene.add(earthGroup);

const controls = new OrbitControls(camera, renderer.domElement);
controls.rotateSpeed = 0.25;

const detail = 12;
const loader = new THREE.TextureLoader();
const geometry = new THREE.IcosahedronGeometry(1, detail);

// Modified main Earth material to avoid shadows
const material = new THREE.MeshStandardMaterial({
    map: loader.load("./static/textures/8k_earth_daymap.jpg"),
    bumpMap: loader.load("./static/textures/01_earthbump1k.jpg"),
    bumpScale: 0.1,
    // Using StandardMaterial with adjustments to avoid shadows
    roughness: 1.8,
    metalness: 0.1
});

const earthMesh = new THREE.Mesh(geometry, material);
earthGroup.add(earthMesh);

// Enable casting and receiving shadows only for Earth
earthMesh.castShadow = true;
earthMesh.receiveShadow = true;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

// Create spotlight to cast shadow from top-left to bottom-right
const shadowLight = new THREE.SpotLight(0xffffff, 1.2);
shadowLight.angle = Math.PI / 5;
shadowLight.penumbra = 0.7;
shadowLight.decay = 2;
shadowLight.distance = 10;

// Position it diagonally (top-left of globe)
shadowLight.position.set(-3, 3, 3);
shadowLight.target = earthMesh;
shadowLight.castShadow = true;

// Optional: soften shadow resolution
shadowLight.shadow.mapSize.width = 1024;
shadowLight.shadow.mapSize.height = 1024;
shadowLight.shadow.radius = 4;

scene.add(shadowLight);
scene.add(shadowLight.target);

// Removed nightside lights mesh

const cloudsMat = new THREE.MeshStandardMaterial({
    map: loader.load("./static/textures/8k_earth_clouds.jpg"),
    transparent: true,
    opacity: 0.8,
    blending: THREE.AdditiveBlending,
    alphaMap: loader.load('./static/textures/05_earthcloudmaptrans.jpg'),
    // alphaTest: 0.3,
});
const cloudsMesh = new THREE.Mesh(geometry, cloudsMat);
cloudsMesh.scale.setScalar(1.003);
earthGroup.add(cloudsMesh);

const fresnelMat = getFresnelMat();
const glowMesh = new THREE.Mesh(geometry, fresnelMat);
glowMesh.scale.setScalar(1.01);
earthGroup.add(glowMesh);

const stars = getStarfield({numStars: 2000});
scene.add(stars);

// Create a light that will follow the camera
const sunLight = new THREE.DirectionalLight(0xffffff, 1.5);
scene.add(sunLight);

// Add ambient light to eliminate shadows
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

// Add a hemisphere light to better illuminate without shadows
const hemisphereLight = new THREE.HemisphereLight(0xffffff, 0x404040, 0.8);
scene.add(hemisphereLight);

function animate() {
    requestAnimationFrame(animate);

    // Update sunLight position to match camera position
    // This makes the light come from the same direction as the camera
    sunLight.position.copy(camera.position);
    
    // Keep stars slowly rotating for visual effect
    stars.rotation.y -= 0.0005;

    // Calculate camera distance to Earth's center
    const distance = camera.position.length();

    // Adjust cloud opacity based on distance
    const fadeStart = 1.7; // start fading when closer than this
    const fadeEnd = 1.3;   // fully disappear when closer than this

    if (distance < fadeStart) {
        const t = THREE.MathUtils.clamp((distance - fadeEnd) / (fadeStart - fadeEnd), 0, 1);
        cloudsMesh.material.opacity = t * 0.8; // original opacity was 0.8
    } else {
        cloudsMesh.material.opacity = 0.8;
    }
    
    composer.render();
}

// Create postprocessing pipeline
const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));

// Screen-space shadow pass
const shadowShader = {
    uniforms: {
        tDiffuse: { value: null },
        uStrength: { value: 0.75 } // Adjust strength of shadow effect
    },
    vertexShader: `
        varying vec2 vUv;
        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform sampler2D tDiffuse;
        uniform float uStrength;
        varying vec2 vUv;

        void main() {
            vec4 texColor = texture2D(tDiffuse, vUv);
            
            // Make a radial shadow in bottom-right corner
            vec2 center = vec2(0.8, 0.2);
            float dist = distance(vUv, center);
            float shadow = smoothstep(0.5, 0.2, dist); // soft radial falloff

            vec3 finalColor = mix(texColor.rgb, vec3(0.0), shadow * uStrength);
            gl_FragColor = vec4(finalColor, texColor.a);
        }
    `
};

const shadowPass = new ShaderPass(shadowShader);
composer.addPass(shadowPass);


animate();

function handleWindowResize () {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}
window.addEventListener('resize', handleWindowResize, false);