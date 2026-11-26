// Futgoat · Campo 3D — the style's engine. A tilted 3D pitch, numbered discs for players, dashed run/pass arrows,
// highlighted zones and formation bars. Pure: everything is placed by the caller from t; render() draws one frame.
// Units: metres. Pitch x = length (0 = our goal, attack towards +x), z = width (0 = left touchline seen from our goal).
import * as THREE from '/node_modules/three/build/three.module.js';
export const PAL = { bg: 0x111111, ouro: 0xD4A537, creme: 0xF2E9D8, bronze: 0x8A5A12, grafite: 0x2A2A2E, cinza: 0x3A3A3C };   // the Futgoat palette: warm black, gold, cream, bronze
export const TEAM = [ // [top fill, side, number ink]
  ['#D4A537', 0xA8832B, '#111111'],  // 0 · our team (gold)
  ['#F2E9D8', 0xCFC5B0, '#111111'],  // 1 · opponent (cream)
  ['#8A5A12', 0x6A430D, '#F2E9D8'],  // 2 · bronze
  ['#2A2A2E', 0x1B1B1E, '#D4A537'],  // 3 · graphite
];
export const PITCH = { society: [40, 24], campo: [105, 68], futsal: [40, 20] };
export function createCampo(canvas, { W = 1080, H = 1920, kind = 'society' } = {}) {
  const [PL, PW] = PITCH[kind];
  const r = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  r.setSize(W, H, false); r.shadowMap.enabled = true; r.shadowMap.type = THREE.PCFSoftShadowMap; r.outputColorSpace = THREE.SRGBColorSpace;
  const scene = new THREE.Scene(); scene.background = new THREE.Color(PAL.bg); scene.fog = new THREE.Fog(PAL.bg, PL * 4, PL * 8);
  const cam = new THREE.PerspectiveCamera(32, W / H, .1, PL * 10);
  scene.add(new THREE.HemisphereLight(0xfff4e0, 0x1a1a1c, 1.5));
  const sun = new THREE.DirectionalLight(0xffffff, 2.2); sun.position.set(-PL * .45, PL, PL * .55); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -PL, right: PL, top: PL, bottom: -PL, far: PL * 4 }); scene.add(sun);
  // board: hi-res canvas with faint stripes, a technical dotted grid and hairline cream markings (0.07 m, like a real pitch)
  const S = 100, tc = document.createElement('canvas'); tc.width = PL * S; tc.height = PW * S; const g = tc.getContext('2d');
  const nS = 10; for (let i = 0; i < nS; i++) { g.fillStyle = i % 2 ? '#26272B' : '#202125'; g.fillRect(i * tc.width / nS, 0, tc.width / nS + 1, tc.height); }
  g.fillStyle = 'rgba(242,233,216,.10)'; for (let x = 5; x < PL; x += 5) for (let z = 5; z < PW; z += 5) { g.beginPath(); g.arc(x * S, z * S, S * .035, 0, 7); g.fill(); }   // 5 m dotted grid, a drawing-board detail
  const LW = S * .07; g.strokeStyle = 'rgba(242,233,216,.92)'; g.fillStyle = 'rgba(242,233,216,.92)'; g.lineWidth = LW;
  const m = LW / 2; g.strokeRect(m, m, tc.width - 2 * m, tc.height - 2 * m);
  g.beginPath(); g.moveTo(tc.width / 2, 0); g.lineTo(tc.width / 2, tc.height); g.stroke();
  const cr = (kind === 'campo' ? 9.15 : 3) * S; g.beginPath(); g.arc(tc.width / 2, tc.height / 2, cr, 0, 7); g.stroke(); g.beginPath(); g.arc(tc.width / 2, tc.height / 2, S * .18, 0, 7); g.fill();
  const box = kind === 'campo' ? [16.5, 40.3] : [6, 12], spot = kind === 'campo' ? 11 : 6, sbox = kind === 'campo' ? [5.5, 18.3] : [2.2, 5];
  for (const s of [0, 1]) { const x0 = s ? tc.width : 0, d = s ? -1 : 1;
    g.strokeRect(Math.min(x0, x0 + d * box[0] * S), tc.height / 2 - box[1] / 2 * S, box[0] * S, box[1] * S);            // penalty area
    g.strokeRect(Math.min(x0, x0 + d * sbox[0] * S), tc.height / 2 - sbox[1] / 2 * S, sbox[0] * S, sbox[1] * S);        // goal area
    g.beginPath(); g.arc(x0 + d * spot * S, tc.height / 2, S * .14, 0, 7); g.fill();                                       // penalty spot
    g.beginPath(); g.arc(x0 + d * spot * S, tc.height / 2, (kind === 'campo' ? 9.15 : 3) * S, d > 0 ? -.93 : Math.PI - .93, d > 0 ? .93 : Math.PI + .93); g.stroke();   // penalty arc
    for (const zz of [0, 1]) { g.beginPath(); g.arc(x0, zz * tc.height, S * 1, zz ? (s ? Math.PI : Math.PI * 1.5) : (s ? Math.PI / 2 : 0), zz ? (s ? Math.PI * 1.5 : Math.PI * 2) : (s ? Math.PI : Math.PI / 2)); g.stroke(); }   // corner arcs
  }
  const tex = new THREE.CanvasTexture(tc); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  const edge = new THREE.MeshStandardMaterial({ color: 0x17181B, roughness: 1 });
  const pitch = new THREE.Mesh(new THREE.BoxGeometry(PL, 1, PW), [edge, edge, new THREE.MeshStandardMaterial({ map: tex, roughness: .95 }), edge, edge, edge]);
  pitch.position.y = -.5; pitch.receiveShadow = true; scene.add(pitch);
  const apron = new THREE.Mesh(new THREE.BoxGeometry(PL + 4, .9, PW + 4), edge); apron.position.y = -.56; apron.receiveShadow = true; scene.add(apron);
  const P = (x, z, y = 0) => new THREE.Vector3(x - PL / 2, y, z - PW / 2);
  const R = PL / 40;   // disc radius scales with the pitch
  const numTex = (n, bg, fg) => { const c = document.createElement('canvas'); c.width = c.height = 512; const k = c.getContext('2d'); k.fillStyle = bg; k.fillRect(0, 0, 512, 512); k.fillStyle = fg; k.font = '330px Anton'; k.textAlign = 'center'; k.textBaseline = 'middle'; k.fillText(String(n), 256, 282); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; };
  const api = { THREE, scene, cam, renderer: r, P, PL, PW, R, tokens: [] };
  // a player: a disc with a number; place it with tok.at(x, z, lift), spin the number to the camera with tok.face(az)
  api.token = (n, team = 0) => {
    const [bg, side, fg] = TEAM[team];
    const sm = new THREE.MeshStandardMaterial({ color: side, roughness: .5 }), tm = new THREE.MeshStandardMaterial({ map: numTex(n, bg, fg), roughness: .45 });
    const d = new THREE.Mesh(new THREE.CylinderGeometry(R, R, R * .36, 64), [sm, tm, sm]); d.castShadow = true;
    const ring = new THREE.Mesh(new THREE.TorusGeometry(R, R * .025, 8, 64), new THREE.MeshStandardMaterial({ color: 0x111111 })); ring.rotation.x = Math.PI / 2; ring.position.y = R * .24; d.add(ring);
    const ring2 = new THREE.Mesh(new THREE.TorusGeometry(R * .84, R * .018, 8, 64), new THREE.MeshBasicMaterial({ color: new THREE.Color(fg) })); ring2.rotation.x = Math.PI / 2; ring2.position.y = R * .245; d.add(ring2);   // fine inner ring
    scene.add(d);
    const tok = { n, team, mesh: d, at(x, z, lift = 0, s = 1) { d.position.copy(P(x, z, R * .24 + lift)); d.scale.setScalar(s); d.visible = s > .01; return tok; }, face(az) { d.rotation.y = az; return tok; } };
    api.tokens.push(tok); return tok;
  };
  api.ball = (() => { const b = new THREE.Mesh(new THREE.SphereGeometry(R * .36, 24, 16), new THREE.MeshStandardMaterial({ color: 0xF2E9D8, roughness: .4 })); b.castShadow = true; scene.add(b);
    return { mesh: b, at(x, z, h = 0) { b.position.copy(P(x, z, R * .36 + h)); return this; } }; })();
  // dashed arrow along points [[x,z],…]; arrow.reveal(p) draws it up to p (0..1)
  api.arrow = (pts, color = PAL.ouro, w = R * .075) => {
    const curve = new THREE.CatmullRomCurve3(pts.map(([x, z]) => P(x, z, .06))); const grp = new THREE.Group(); const N = Math.max(12, Math.round(curve.getLength() / (R * .5)));
    for (let i = 0; i < N; i += 2) { const a = curve.getPoint(i / N), b = curve.getPoint(Math.min(1, (i + 1) / N)), dv = b.clone().sub(a);
      const s = new THREE.Mesh(new THREE.BoxGeometry(dv.length(), .04, w), new THREE.MeshBasicMaterial({ color })); s.position.copy(a.clone().add(b).multiplyScalar(.5)); s.rotation.y = -Math.atan2(dv.z, dv.x); s.userData.u = (i + 1) / N; grp.add(s); }
    const e = curve.getPoint(1), tn = curve.getTangent(1);
    const head = new THREE.Mesh(new THREE.ConeGeometry(w * 3.2, w * 9, 3), new THREE.MeshBasicMaterial({ color })); head.rotation.z = -Math.PI / 2;
    const hg = new THREE.Group(); hg.add(head); hg.position.copy(e).setY(.08); hg.rotation.y = -Math.atan2(tn.z, tn.x); hg.scale.y = .1; hg.userData.u = 1; grp.add(hg);
    const dot = new THREE.Mesh(new THREE.CircleGeometry(w * 2.4, 24), new THREE.MeshBasicMaterial({ color })); dot.rotation.x = -Math.PI / 2; dot.position.copy(curve.getPoint(0)).setY(.07); dot.userData.u = .001; grp.add(dot);   // start marker
    scene.add(grp); grp.reveal = (p) => grp.children.forEach(c => c.visible = p > 0 && c.userData.u <= p + 1e-6); grp.reveal(0); return grp;
  };
  // a highlighted space (circle) or a formation bar (a soft band through points)
  api.zone = (x, z, rad, color = PAL.ouro) => { const ringZ = new THREE.Mesh(new THREE.RingGeometry(rad - .06, rad, 96), new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0, depthWrite: false })); ringZ.rotation.x = -Math.PI / 2; ringZ.position.copy(P(x, z, .035)); scene.add(ringZ); const mz = new THREE.Mesh(new THREE.CircleGeometry(rad, 64), new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0, depthWrite: false })); mz.rotation.x = -Math.PI / 2; mz.position.copy(P(x, z, .03)); scene.add(mz); mz.show = (a) => { mz.material.opacity = .14 * a; mz.visible = a > 0; ringZ.material.opacity = .8 * a; ringZ.visible = a > 0; }; mz.show(0); return mz; };
  api.bar = (pts, color = PAL.ouro) => { const grp = new THREE.Group(); for (let i = 0; i < pts.length - 1; i++) { const a = P(...pts[i], .02), b = P(...pts[i + 1], .02), dv = b.clone().sub(a);
      const s = new THREE.Mesh(new THREE.BoxGeometry(dv.length(), .02, R * .35), new THREE.MeshBasicMaterial({ color, transparent: true, opacity: .3, depthWrite: false })); s.position.copy(a.clone().add(b).multiplyScalar(.5)); s.rotation.y = -Math.atan2(dv.z, dv.x); grp.add(s); }
    scene.add(grp); grp.show = (a) => { grp.children.forEach(c => c.material.opacity = .3 * a); grp.visible = a > 0; }; grp.show(0); return grp; };
  // camera on a sphere around a target: az 0 = behind our goal looking up the pitch; el = height angle; d = distance
  api.view = ({ x, z, az = 0, el = 1.1, d = 90 }) => { const t = P(x, z); cam.position.set(t.x - Math.cos(el) * Math.cos(az) * d, Math.sin(el) * d, t.z + Math.cos(el) * Math.sin(az) * d); cam.up.set(0, 1, 0); cam.lookAt(t); api.tokens.forEach(k => k.face(az)); return az; };
  api.render = () => r.render(scene, cam);
  return api;
}
