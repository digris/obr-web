/* eslint max-classes-per-file: ["error", 10] */

/*
import { Scene } from 'three/src/scenes/Scene';
import { PerspectiveCamera } from 'three/src/cameras/PerspectiveCamera';
import { WebGLRenderer } from 'three/src/renderers/WebGLRenderer';
import { Mesh } from 'three/src/objects/Mesh';
import { BoxGeometry } from 'three/src/geometries/BoxGeometry';
import { MeshNormalMaterial } from 'three/src/materials/MeshNormalMaterial';
*/

import {
  Scene,
  PerspectiveCamera,
  WebGLRenderer,
  Mesh,
  BoxGeometry,
  // MeshNormalMaterial,
  MeshLambertMaterial,
  // ShaderMaterial,
  // TextureLoader,
  // AdditiveBlending,
  //
  // BufferGeometry,
  // BufferAttribute,
  //
  AmbientLight,
  DirectionalLight,
  PointLight,
  //
  SphereGeometry,
  MeshBasicMaterial,
} from 'three';

class Starfield {
  // ctx: CanvasRenderingContext2D|null;

  animationId: number = -1;

  width: number;

  height: number;

  scene: Scene;

  mesh: Mesh;

  camera: PerspectiveCamera;

  renderer: WebGLRenderer;

  lastRenderTime: number = 0;

  constructor(canvas: HTMLCanvasElement) {
    const { width, height } = canvas;
    const camera = new PerspectiveCamera(30, width / height, 0.01, 10);
    const scene = new Scene();
    const geometry = new BoxGeometry(0.2, 0.2, 0.2);
    const material = new MeshLambertMaterial({
      color: 0xffffff,
    });

    const ambientLight = new AmbientLight(0x111111);
    scene.add(ambientLight);

    const directionalLight = new DirectionalLight(0xffffff, 1.0);
    directionalLight.position.x = Math.random() - 0.5;
    directionalLight.position.y = Math.random() - 0.5;
    directionalLight.position.z = Math.random() - 0.5;
    directionalLight.position.normalize();
    scene.add(directionalLight);

    const pointLight = new PointLight(0xffffff, 10);
    scene.add(pointLight);

    pointLight.add(
      new Mesh(
        new SphereGeometry(4, 8, 8),
        new MeshBasicMaterial({ color: 0xffffff }),
      ),
    );

    /*
    const geometry = new BufferGeometry();
    geometry.setAttribute('position', new BufferAttribute(positions, 3));
    geometry.addAttribute('color', new THREE.BufferAttribute(colors, 3));
    geometry.addAttribute('size', new THREE.BufferAttribute(sizes, 1));
    geometry.addAttribute('rotation', new THREE.BufferAttribute(rotations, 1));
    geometry.addAttribute('sCoef', new THREE.BufferAttribute(sCoef, 1));
    const material = new ShaderMaterial({
      uniforms: {
        uTime: { value: 0 },
        uTexture: { value: new TextureLoader().load('https://klevron.github.io/codepen/misc/star.png') },
      },
      vertexShader: `
      uniform float uTime;
      uniform vec2 uMouse;
      attribute vec3 color;
      attribute float size;
      attribute float rotation;
      attribute float sCoef;
      varying vec4 vColor;
      varying float vRotation;
      void main() {
        vColor = vec4(color, 1.);
        vRotation = rotation;

        vec3 p = vec3(position);
        p.z = -1000. + mod(position.z + uTime*(sCoef*50.*0.1), 2000.);
        //p.x = -500. + mod(position.x - uTime*(sCoef*50.*uMouse.x), 1000.);

        vec4 mvPosition = modelViewMatrix * vec4(p, 1.);
        gl_Position = projectionMatrix * mvPosition;

        float psize = size * (200. / -mvPosition.z);
        gl_PointSize = psize * (1. + .5*sin(uTime*sCoef + position.x));
      }
    `,
      fragmentShader: `
      uniform sampler2D uTexture;
      varying vec4 vColor;
      varying float vRotation;
      void main() {
        vec2 v = gl_PointCoord - .5;
        float ca = cos(vRotation), sa = sin(vRotation);
        mat2 rmat = mat2(ca, -sa, sa, ca);
        gl_FragColor = vColor * texture2D(uTexture, v*rmat + .5);
      }
    `,
      blending: AdditiveBlending,
      depthTest: false,
      transparent: true,
    });
    */

    const mesh = new Mesh(geometry, material);

    const renderer = new WebGLRenderer({
      canvas,
      alpha: true,
      antialias: true,
    });
    renderer.setSize(width, height);

    camera.position.z = 1;
    scene.add(mesh);

    this.width = width;
    this.height = height;
    this.scene = scene;
    this.mesh = mesh;
    this.camera = camera;
    this.renderer = renderer;
    this.start();
  }

  start = () => {
    this.renderer.setAnimationLoop(this.run);
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  run = (time: number) => {
    this.mesh.rotation.x = time / 2000;
    this.mesh.rotation.y = time / 1000;
    this.render();
  }

  render = () => {
    this.renderer.render(this.scene, this.camera);
  }
}

export { Starfield };
