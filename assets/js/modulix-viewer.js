// Modulix configurator: one module, many pieces of furniture.
// Loads the module and cushion meshes once (modulix-single.glb holds all of them),
// builds every configuration in the browser, and animates between them with a hop.
import * as THREE from 'three';
import { GLTFLoader } from './three/GLTFLoader.js';
import { OrbitControls } from './three/OrbitControls.js';
import { RoomEnvironment } from './three/RoomEnvironment.js';

const root = document.getElementById('mod-config');
const stage = root.querySelector('.cfg-stage');
const capEl = root.querySelector('#mod-cap');
const tabs = [...root.querySelectorAll('[role="tab"]')];
const dice = root.querySelector('.cfg-dice');
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

// ---------------------------------------------------------------- transforms
const PI2 = Math.PI / 2;
const T = (x = 0, y = 0, z = 0) => new THREE.Matrix4().makeTranslation(x, y, z);
const RY = (a = PI2) => new THREE.Matrix4().makeRotationY(a);
const RZ = (a = PI2) => new THREE.Matrix4().makeRotationZ(a);
const RX = (a) => new THREE.Matrix4().makeRotationX(a);
const M = (...ms) => ms.reduce((a, b) => a.multiply(b), new THREE.Matrix4());

let W, H, D; // module extents: width (x), height (y), length along the tube (z)

// One layout = list of {t: part type, m: Matrix4}. Builders work in local
// coordinates; place() moves a whole group (e.g. a chair) into position.
const P = (t, m) => ({ t, m });
const place = (G, parts) => parts.map(p => P(p.t, G.clone().multiply(p.m)));

const seat = (x, z = 0) => P('module', M(T(x, 0, z), RY()));                 // lying, openings to the sides
const table = (x, z = 0) => P('module', T(x, 0, z));                          // lying, openings front and back
const arm = (x, z = 0, side = 1) => P('module', M(T(x, 0, z), T(0, W / 2, 0), RZ(side < 0 ? -PI2 : PI2), T(0, -H / 2, 0)));
const back = (x, zSeat = 0) => P('module', M(T(x, 0, zSeat - W / 2 - H / 2), RY(), T(0, W / 2, 0), RZ(), T(0, -H / 2, 0)));
const seatCush = (x, z = 0) => P('seat', T(x, H + 0.06, z));
const backCush = (x, zSeat = 0) => P('back', M(T(x, H + 0.12 + 0.19, zSeat - W / 2 + 0.1), RX(THREE.MathUtils.degToRad(-10))));
const prop = (t, x, y, z, a = 0) => P(t, M(T(x, y, z), RY(a)));

// a row of n seats with backrests, cushions and optional armrests
function sofa(n, { arms = [true, true] } = {}) {
  const p = [];
  for (let i = 0; i < n; i++) {
    const x = (i - (n - 1) / 2) * D;
    p.push(seat(x), back(x), seatCush(x), backCush(x));
  }
  const ax = n * D / 2 + H / 2;
  if (arms[0]) p.push(arm(-ax, 0, -1));
  if (arms[1]) p.push(arm(ax, 0, 1));
  return p;
}
const armTop = (n, side, front = 0.13) => [side * (n * D / 2 + H / 2), W, front]; // where a cup sits on an armrest

function lounger() { // two seats end to end, an upright backrest, full-length mattress
  return place(T(-D / 2, 0, 0), [
    seat(0), seat(D), arm(-(D / 2 + H / 2), 0, -1),
    P('lounge', T(D / 2, H + 0.05, 0)), P('lback', T(-D / 2 + 0.06, H + 0.10 + 0.23, 0)),
  ]);
}

// ---------------------------------------------------------------- layouts
const pick = (rng, a) => a[Math.floor(rng() * a.length)];
const LAYOUTS = {
  sofa: { cap: 'Two seat modules with upright modules as armrests and backrest, plus cushions.', build: () => sofa(2) },
  table: { cap: 'One module as a side table or stool.', build: () => [table(0)] },
  lounger: { cap: 'Two modules end to end with an upright backrest and a full-length cushion.', build: lounger },
  stack: {
    cap: 'One stack for winter, with the cushions stored inside each module.',
    build: () => {
      const p = [];
      for (let i = 0; i < 4; i++) {
        const y = i * (H + 0.004);
        p.push(P('module', T(0, y, 0)), P('store', T(0, y + 0.0775, 0)), P('store', T(0, y + 0.1955, 0)));
      }
      return p;
    },
  },
};

// The dice only rolls these. Props vary on every roll.
const DICE = {
  armchairs: {
    cap: 'Two armchairs angled towards each other, with a cup on an armrest.',
    build: (rng) => {
      const a = 0.2, x = 0.8;
      const chair = sofa(1);
      const side = pick(rng, [-1, 1]), which = pick(rng, [-1, 1]);
      const [cx, cy, cz] = armTop(1, side);
      return [
        ...place(M(T(-x, 0, 0), RY(a)), which < 0 ? [...chair, prop('cup', cx, cy, cz, rng() * 6)] : chair),
        ...place(M(T(x, 0, 0), RY(-a)), which > 0 ? [...chair, prop('cup', cx, cy, cz, rng() * 6)] : chair),
      ];
    },
  },
  sofaTable: {
    cap: 'A sofa with a side table and flowers.',
    build: (rng) => {
      const sx = -(H + W / 2 + 0.06) / 2, side = pick(rng, [-1, 1]);
      const tx = side * (D + H + 0.06 + W / 2);
      return place(T(side * sx, 0, 0), [...sofa(2), table(tx, -0.02), prop('vase', tx + 0.05, H, -0.05, rng() * 6)]);
    },
  },
  threeSeater: {
    cap: 'A three-seat sofa from nine modules.',
    build: (rng) => {
      const p = sofa(3);
      if (rng() < 0.7) { const [x, y, z] = armTop(3, pick(rng, [-1, 1])); p.push(prop('cup', x, y, z, rng() * 6)); }
      return p;
    },
  },
  loungerTable: {
    cap: 'A sun lounger with a side table.',
    build: (rng) => {
      const tz = W / 2 + 0.1 + D / 2, tx = -D / 2 - 0.1;
      const props = pick(rng, [
        [prop('cup', tx - 0.12, H, tz + 0.1, rng() * 6), prop('book', tx + 0.12, H, tz - 0.05, rng() - 0.5)],
        [prop('vase', tx, H, tz, rng() * 6)],
        [prop('cup', tx + 0.1, H, tz + 0.12, rng() * 6), prop('vase', tx - 0.1, H, tz - 0.1, rng() * 6)],
      ]);
      return [...lounger(), table(tx, tz), ...props];
    },
  },
  twoLoungers: {
    cap: 'Two sun loungers with a table and flowers between them.',
    build: (rng) => {
      const z = D / 2 + 0.08 + W / 2, tx = -D / 2 - 0.15;
      return [
        ...place(T(0, 0, -z), lounger()), ...place(T(0, 0, z), lounger()),
        P('module', M(T(tx, 0, 0), RY())),
        prop('vase', tx - 0.08, H, -0.06, rng() * 6), ...(rng() < 0.6 ? [prop('cup', tx + 0.15, H, 0.12, rng() * 6)] : []),
      ];
    },
  },
  chairStool: {
    cap: 'An armchair with a footstool, and a cup on the armrest.',
    build: (rng) => {
      const [x, y, z] = armTop(1, pick(rng, [-1, 1]));
      const oz = W + 0.2;
      return [...sofa(1), seat(0, oz), seatCush(0, oz), prop('cup', x, y, z, rng() * 6),
        ...(rng() < 0.5 ? [prop('book', 0.12, H + 0.12, oz + 0.05, rng() - 0.5)] : [])];
    },
  },
  bench: {
    cap: 'A bench of two seats with a plant table at the end.',
    build: (rng) => {
      const side = pick(rng, [-1, 1]), tx = side * (D + W / 2 + 0.04);
      return place(T(-side * (W / 2 + 0.04) / 2, 0, 0), [
        seat(-D / 2), seat(D / 2), seatCush(-D / 2), seatCush(D / 2),
        table(tx), prop('plant', tx, H, 0, rng() * 6),
      ]);
    },
  },
  coffee: {
    cap: 'A sofa with a coffee table, cups and flowers.',
    build: (rng) => {
      const tz = W / 2 + 0.45 + W / 2;
      return [...sofa(2), seat(0, tz),
        prop('vase', -0.12, H, tz - 0.06, rng() * 6), prop('cup', 0.14, H, tz + 0.1, rng() * 6),
        ...(rng() < 0.6 ? [prop('cup', 0.2, H, tz - 0.12, rng() * 6)] : [])];
    },
  },
  chaise: {
    cap: 'A chaise sofa, with one extra seat module in front.',
    build: (rng) => {
      const side = pick(rng, [-1, 1]), cx = side * D / 2, cz = W;
      const [x, y, z] = armTop(2, -side);
      return [...sofa(2), seat(cx, cz), seatCush(cx, cz), prop('cup', x, y, z, rng() * 6),
        ...(rng() < 0.5 ? [prop('book', cx, H + 0.12, cz + 0.05, rng() - 0.5)] : [])];
    },
  },
};

// ---------------------------------------------------------------- props (drawn in code)
function lathe(points, mat, segs = 40) {
  const g = new THREE.LatheGeometry(points.map(([r, y]) => new THREE.Vector2(r, y)), segs);
  const m = new THREE.Mesh(g, mat); m.castShadow = true; return m;
}
function makeProps() {
  const ceramic = new THREE.MeshStandardMaterial({ color: 0xF1EEE7, roughness: 0.35 });
  const coffee = new THREE.MeshStandardMaterial({ color: 0x3B2A20, roughness: 0.3 });
  const stem = new THREE.MeshStandardMaterial({ color: 0x5E6B4B, roughness: 0.8 });
  const leaf = new THREE.MeshStandardMaterial({ color: 0x55704A, roughness: 0.7, side: THREE.DoubleSide });
  const terracotta = new THREE.MeshStandardMaterial({ color: 0xB86E50, roughness: 0.85 });
  const glass = new THREE.MeshStandardMaterial({ color: 0x8FA9C9, roughness: 0.15, metalness: 0, transparent: true, opacity: 0.55 });
  const petals = [0xF3EBDD, 0xE9C9A8, 0xF0D27A].map(c => new THREE.MeshStandardMaterial({ color: c, roughness: 0.7 }));

  const cup = new THREE.Group();
  cup.add(lathe([[0, 0], [0.03, 0], [0.036, 0.01], [0.04, 0.085], [0.036, 0.085], [0.033, 0.012], [0, 0.012]], ceramic));
  const fill = new THREE.Mesh(new THREE.CircleGeometry(0.035, 32), coffee); fill.rotation.x = -PI2; fill.position.y = 0.07; cup.add(fill);
  const handle = new THREE.Mesh(new THREE.TorusGeometry(0.02, 0.005, 10, 24, Math.PI), ceramic);
  handle.rotation.z = -PI2; handle.position.set(0.04, 0.045, 0); handle.castShadow = true; cup.add(handle);

  const vase = new THREE.Group();
  vase.add(lathe([[0, 0], [0.045, 0], [0.065, 0.06], [0.06, 0.14], [0.035, 0.2], [0.04, 0.22], [0.033, 0.22], [0.03, 0.2], [0.055, 0.14], [0.058, 0.06], [0.04, 0.008], [0, 0.008]], glass));
  for (let i = 0; i < 7; i++) {
    const a = i / 7 * Math.PI * 2, tilt = 0.12 + (i % 3) * 0.08, len = 0.28 + (i % 4) * 0.04;
    const s = new THREE.Group(); s.position.y = 0.08; s.rotation.set(Math.cos(a) * tilt, 0, Math.sin(a) * tilt);
    const st = new THREE.Mesh(new THREE.CylinderGeometry(0.0025, 0.003, len, 6), stem); st.position.y = len / 2; s.add(st);
    const head = new THREE.Mesh(new THREE.IcosahedronGeometry(0.022, 1), petals[i % 3]); head.position.y = len; head.scale.set(1, 0.7, 1); head.castShadow = true; s.add(head);
    vase.add(s);
  }

  const plant = new THREE.Group();
  plant.add(lathe([[0, 0], [0.08, 0], [0.11, 0.2], [0.12, 0.2], [0.12, 0.215], [0.1, 0.215], [0.07, 0.02], [0, 0.02]], terracotta));
  const soil = new THREE.Mesh(new THREE.CircleGeometry(0.1, 24), coffee); soil.rotation.x = -PI2; soil.position.y = 0.19; plant.add(soil);
  const leafGeo = new THREE.SphereGeometry(1, 12, 8); leafGeo.scale(0.035, 0.2, 0.012); leafGeo.translate(0, 0.2, 0);
  for (let i = 0; i < 14; i++) {
    const l = new THREE.Mesh(leafGeo, leaf); const a = i * 2.4, k = 0.2 + (i % 4) * 0.12;
    l.position.y = 0.19; l.rotation.set(Math.cos(a) * k, a, Math.sin(a) * k); l.scale.setScalar(0.8 + (i % 3) * 0.2); l.castShadow = true; plant.add(l);
  }

  const book = new THREE.Group();
  [[0x5A6E7F, 0], [0xC9B79C, 0.026]].forEach(([c, y], i) => {
    const b = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.024, 0.21), new THREE.MeshStandardMaterial({ color: c, roughness: 0.8 }));
    b.position.set(i * 0.01, y + 0.012, i * -0.008); b.rotation.y = i * 0.12; b.castShadow = true; book.add(b);
  });
  return { cup, vase, plant, book };
}

// ---------------------------------------------------------------- scene
let renderer, scene, camera, controls, sun, ground, lib = {}, boxes = {};
let live = []; // {t, obj, anim}
let current = null, history = [];

function setup() {
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 0.92;
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  stage.appendChild(renderer.domElement);
  scene = new THREE.Scene();
  const pm = new THREE.PMREMGenerator(renderer);
  scene.environment = pm.fromScene(new RoomEnvironment(renderer), 0.04).texture;
  scene.add(new THREE.HemisphereLight(0xffffff, 0xd8d4cc, 0.6));
  sun = new THREE.DirectionalLight(0xffffff, 1.6); sun.position.set(2.6, 3.4, 1.6); sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048); sun.shadow.bias = -0.0004; sun.shadow.radius = 4;
  scene.add(sun, sun.target);
  ground = new THREE.Mesh(new THREE.PlaneGeometry(30, 30), new THREE.ShadowMaterial({ opacity: 0.2 }));
  ground.rotation.x = -PI2; ground.receiveShadow = true; scene.add(ground);
  camera = new THREE.PerspectiveCamera(30, 1, 0.05, 60);
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true; controls.enableZoom = false; controls.enablePan = false;
  controls.minPolarAngle = 0.2; controls.maxPolarAngle = 1.45;
  renderer.domElement.style.touchAction = 'pan-y';
  const sph = new THREE.Spherical(6, THREE.MathUtils.degToRad(68), THREE.MathUtils.degToRad(35));
  camera.position.setFromSpherical(sph);
  new ResizeObserver(resize).observe(stage); resize();
}
function resize() {
  const w = stage.clientWidth, h = stage.clientHeight; if (!w || !h) return;
  renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
  if (current) frame(current.parts, false);
}

async function loadLibrary() {
  const loader = new GLTFLoader();
  let gltf;
  try { gltf = await loader.loadAsync(root.dataset.src); }
  catch (e) { if (!root.dataset.alt) throw e; gltf = await loader.loadAsync(root.dataset.alt); }
  const meshes = gltf.parser.json.meshes;
  for (let i = 0; i < meshes.length; i++) {
    const m = await gltf.parser.getDependency('mesh', i);
    m.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; o.geometry.computeBoundingBox(); } });
    lib[meshes[i].name] = m;
    const g = m.isMesh ? m.geometry : m.children[0].geometry;
    boxes[meshes[i].name] = g.boundingBox.clone();
  }
  // cushions in the dark grey outdoor fabric seen on the model
  const fabric = new THREE.MeshStandardMaterial({ color: 0x4A4D51, roughness: 1 });
  for (const k of ['seat', 'back', 'lounge', 'lback', 'store']) lib[k].traverse(o => { if (o.isMesh) o.material = fabric; });
  const mb = boxes.module; W = mb.max.x - mb.min.x; H = mb.max.y - mb.min.y; D = mb.max.z - mb.min.z;
  Object.assign(lib, makeProps());
  for (const k of ['cup', 'vase', 'plant', 'book']) boxes[k] = new THREE.Box3().setFromObject(lib[k]);
}

function spawn(t) { const o = lib[t].clone(); o.matrixAutoUpdate = true; scene.add(o); return o; }

// ---------------------------------------------------------------- framing
const tmpBox = new THREE.Box3();
let camAnim = null;
function layoutBox(parts) {
  const b = new THREE.Box3();
  for (const p of parts) b.union(tmpBox.copy(boxes[p.t]).applyMatrix4(p.m));
  return b;
}
function frame(parts, animate = true) {
  const b = layoutBox(parts), c = b.getCenter(new THREE.Vector3()), s = b.getSize(new THREE.Vector3());
  const r = 0.5 * Math.hypot(s.x, s.y, s.z);
  const target = new THREE.Vector3(c.x, c.y, c.z);
  const dist = fitDistance(b, target);
  // shadow camera follows the layout
  const sc = sun.shadow.camera, e = r + 0.6; sc.left = -e; sc.right = e; sc.top = e; sc.bottom = -e; sc.near = 0.5; sc.far = 12; sc.updateProjectionMatrix();
  sun.target.position.copy(target); sun.position.copy(target).add(new THREE.Vector3(2.6, 3.4, 1.6));
  const from = { t: controls.target.clone(), d: camera.position.distanceTo(controls.target) };
  if (!animate || reduceMotion) { applyCam(target, dist); camAnim = null; return; }
  camAnim = { from, to: { t: target, d: dist }, t0: performance.now(), dur: 1100 };
}
// smallest camera distance (from the current viewing angle) that keeps every corner of the box on screen
function fitDistance(b, target) {
  const dir = camera.position.clone().sub(controls.target).normalize();
  const cam = camera.clone(), pts = [];
  for (const x of [b.min.x, b.max.x]) for (const y of [b.min.y, b.max.y]) for (const z of [b.min.z, b.max.z]) pts.push(new THREE.Vector3(x, y, z));
  const fits = (d) => {
    cam.position.copy(target).addScaledVector(dir, d); cam.lookAt(target); cam.updateMatrixWorld(); cam.updateProjectionMatrix();
    return pts.every(p => { const v = p.clone().project(cam); return Math.abs(v.x) < 0.86 && Math.abs(v.y) < 0.8 && v.z < 1; });
  };
  let lo = 0.5, hi = 30;
  for (let i = 0; i < 24; i++) { const mid = (lo + hi) / 2; if (fits(mid)) hi = mid; else lo = mid; }
  return Math.max(1.8, hi);
}
function applyCam(t, d) {
  const dir = camera.position.clone().sub(controls.target).normalize();
  controls.target.copy(t); camera.position.copy(t).addScaledVector(dir, d);
}

// ---------------------------------------------------------------- transitions
const ease = (t) => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
const backOut = (t) => { const c = 1.6; return 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2); };
const ORDER = ['module', 'seat', 'back', 'lounge', 'lback', 'store', 'book', 'cup', 'vase', 'plant'];
const isProp = (t) => ['cup', 'vase', 'plant', 'book'].includes(t);

function decompose(m) { const p = new THREE.Vector3(), q = new THREE.Quaternion(), s = new THREE.Vector3(); m.decompose(p, q, s); return { p, q }; }

let lastShow = 0;
function show(layout, parts, { animate = true } = {}) {
  current = { layout, parts };
  const now = lastShow = performance.now();
  const next = [];
  const pool = {};
  for (const it of live) if (!it.leaving) (pool[it.t] ||= []).push(it);
  const wanted = {};
  for (const p of parts) (wanted[p.t] ||= []).push(p);
  // pair each existing part with the nearest new slot of the same type, shortest pairs first
  for (const t in wanted) {
    const have = pool[t] || [], want = wanted[t], pairs = [];
    have.forEach((h, i) => want.forEach((w, j) => pairs.push([h.obj.position.distanceTo(decompose(w.m).p), i, j])));
    pairs.sort((a, b) => a[0] - b[0]);
    const usedH = new Set(), usedW = new Set(), matched = new Array(want.length);
    for (const [, i, j] of pairs) if (!usedH.has(i) && !usedW.has(j)) { usedH.add(i); usedW.add(j); matched[j] = have[i]; }
    pool[t] = [...matched, ...have.filter((_, i) => !usedH.has(i))];
    pool[t].length = Math.max(want.length, 0) + have.filter((_, i) => !usedH.has(i)).length;
  }
  let order = 0;
  for (const t of ORDER) {
    const want = wanted[t] || [], have = pool[t] || [];
    want.forEach((p, i) => {
      const to = decompose(p.m);
      const delay = isProp(t) ? 520 + order * 45 : order * 55; order++;
      let it = have[i] || null;
      if (it) {
        it.anim = { kind: 'move', p0: it.obj.position.clone(), q0: it.obj.quaternion.clone(), to, t0: now + delay };
      } else {
        it = { t, obj: spawn(t) };
        it.obj.position.copy(to.p).y += 1.0; it.obj.quaternion.copy(to.q); it.obj.scale.setScalar(0.001);
        it.anim = { kind: 'drop', p0: it.obj.position.clone(), q0: to.q.clone(), to, t0: now + delay + 150 };
      }
      it.anim.hop = isProp(t) ? 0.22 : 0.28 + Math.min(0.22, it.anim.p0.distanceTo(to.p) * 0.15);
      it.anim.dur = isProp(t) ? 650 : 820;
      next.push(it);
    });
    have.slice(want.length).filter(Boolean).forEach((it, i) => {
      it.leaving = true;
      it.anim = { kind: 'leave', p0: it.obj.position.clone(), t0: now + i * 40, dur: 420 };
      next.push(it);
    });
  }
  live = next;
  if (!animate || reduceMotion) { for (const it of live) finish(it); live = live.filter(it => !it.gone); }
  frame(parts, animate);
  kick();
}

function finish(it) {
  const a = it.anim; if (!a) return;
  if (a.kind === 'leave') { scene.remove(it.obj); it.gone = true; }
  else { it.obj.position.copy(a.to.p); it.obj.quaternion.copy(a.to.q); it.obj.scale.setScalar(1); }
  it.anim = null;
}

function step(now) {
  let busy = false;
  for (const it of live) {
    const a = it.anim; if (!a) continue; busy = true;
    const u = (now - a.t0) / a.dur;
    if (u < 0) continue;
    const o = it.obj;
    if (a.kind === 'leave') {
      const k = Math.min(1, u);
      o.position.copy(a.p0); o.position.y += Math.sin(k * Math.PI * 0.6) * 0.35;
      o.scale.setScalar(Math.max(0.001, 1 - ease(k)));
      if (u >= 1) finish(it);
      continue;
    }
    if (u < 1) {
      const e = ease(u);
      o.position.lerpVectors(a.p0, a.to.p, e);
      if (a.kind === 'move') o.position.y += Math.sin(Math.PI * u) * a.hop;
      o.quaternion.slerpQuaternions(a.q0, a.to.q, e);
      if (a.kind === 'drop') o.scale.setScalar(Math.max(0.001, backOut(Math.min(1, u * 1.6))));
      else o.scale.setScalar(1);
    } else {
      // landing: a quick squash that settles out
      const v = (now - a.t0 - a.dur) / 1000, amp = isProp(it.t) ? 0.06 : 0.09;
      o.position.copy(a.to.p); o.quaternion.copy(a.to.q);
      const s = amp * Math.exp(-9 * v) * Math.cos(22 * v);
      o.scale.set(1 + s * 0.5, 1 - s, 1 + s * 0.5);
      if (v > 0.6) finish(it);
    }
  }
  live = live.filter(it => !it.gone);
  if (camAnim) {
    const u = Math.min(1, (now - camAnim.t0) / camAnim.dur), e = ease(u);
    applyCam(camAnim.from.t.clone().lerp(camAnim.to.t, e), THREE.MathUtils.lerp(camAnim.from.d, camAnim.to.d, e));
    if (u >= 1) camAnim = null; else busy = true;
  }
  return busy;
}

// render only while something moves or the user is dragging
let raf = 0, idleFrames = 0, inView = true;
function kick() { idleFrames = 0; if (!raf && inView) raf = requestAnimationFrame(loop); }
function loop(now) {
  raf = 0;
  const busy = step(now);
  const moved = controls.update();
  renderer.render(scene, camera);
  idleFrames = busy || moved ? 0 : idleFrames + 1;
  if (idleFrames < 30 && inView) raf = requestAnimationFrame(loop);
}

// ---------------------------------------------------------------- UI
let seed = Date.now() % 100000;
const rng = () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };

function select(name) {
  tabs.forEach(b => b.setAttribute('aria-selected', String(b.dataset.layout === name)));
  const L = LAYOUTS[name]; capEl.textContent = L.cap;
  show(name, L.build(rng));
}
function roll() {
  const names = Object.keys(DICE).filter(n => n !== current?.layout && !history.slice(-3).includes(n));
  const name = pick(rng, names); history.push(name);
  tabs.forEach(b => b.setAttribute('aria-selected', 'false'));
  capEl.textContent = DICE[name].cap;
  dice.classList.remove('rolling'); void dice.offsetWidth; dice.classList.add('rolling');
  show(name, DICE[name].build(rng));
}

async function start() {
  root.classList.add('loading');
  try {
    setup(); await loadLibrary();
  } catch (e) {
    root.classList.remove('loading'); root.classList.add('failed'); console.error(e); return;
  }
  root.classList.remove('loading');
  const first = LAYOUTS.sofa; capEl.textContent = first.cap;
  show('sofa', first.build(rng), { animate: false });
  tabs.forEach(b => b.addEventListener('click', () => select(b.dataset.layout)));
  dice.addEventListener('click', roll);
  controls.addEventListener('start', kick); controls.addEventListener('change', kick);
  new IntersectionObserver(([en]) => { inView = en.isIntersecting; if (inView) kick(); }).observe(stage);
  window.modulix = { show: (n, seedVal) => { if (seedVal != null) seed = seedVal; const L = LAYOUTS[n] || DICE[n]; capEl.textContent = L.cap; show(n, L.build(rng), { animate: false }); }, names: () => [...Object.keys(LAYOUTS), ...Object.keys(DICE)], roll, select,     // test hook: switch with animation, then render the frame `ms` after the switch
    _anim: (n, seedVal) => { if (seedVal != null) seed = seedVal; const L = LAYOUTS[n] || DICE[n]; cancelAnimationFrame(raf); raf = 0; inView = false; show(n, L.build(rng)); },
    _frameAt: (ms) => { step(lastShow + ms); controls.update(); renderer.render(scene, camera); }, settle: () => { for (const it of live) finish(it); live = live.filter(i => !i.gone); camAnim = null; kick(); } };
}

// start loading when the viewer comes near the screen
const io = new IntersectionObserver(([en]) => { if (en.isIntersecting) { io.disconnect(); start(); } }, { rootMargin: '400px' });
io.observe(root);
