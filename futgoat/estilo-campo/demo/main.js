// Demo film of the Futgoat · Campo 3D style (18 s, no voice): the 2-3-1 of society, one move, a goal.
import { createCampo, PAL } from './engine/campo.js';
import { clamp, lerp, seg, eio, eo, ei, back } from '/core/lib.js';
await Promise.all(['40px Anton', '40px Archivo'].map(f => document.fonts.load(f)));
const C = createCampo(document.getElementById('c'), { kind: 'society' });
const ui = document.getElementById('ui');
C.cam.setViewOffset(1080, 1920, 0, -150, 1080, 1920); C.cam.updateProjectionMatrix();   // push the scene below the platforms' top UI
const EV = []; const ev = (t, type, o = {}) => EV.push({ t, type, ...o });
// players: our 2-3-1 (gold) attacking up the pitch, a 2-2-2 (cream)
const A = [[1, 2.5, 12], [2, 10, 6], [3, 10, 18], [5, 18, 12], [7, 19, 3.5], [8, 19, 20.5], [9, 28, 12]];
const B = [[1, 37.5, 12], [4, 31, 8], [6, 31, 16], [8, 24, 7], [10, 24, 17], [9, 15, 12]];
const TA = A.map(([n]) => C.token(n, 0)), TB = B.map(([n]) => C.token(n, 1));
const drop = (i, team) => .25 + i * .12 + team * .9;
A.forEach((_, i) => ev(drop(i, 0) + .32, 'land', { v: .8 })); B.forEach((_, i) => ev(drop(i, 1) + .32, 'land', { v: .6 }));
const bars = [C.bar([[10, 6], [10, 18]]), C.bar([[19, 3.5], [18, 12], [19, 20.5]]), C.bar([[28, 9.5], [28, 14.5]])];
const BAR_T = [2.5, 3.1, 3.7]; BAR_T.forEach(t => ev(t, 'pop'));
const a1 = C.arrow([[18, 12], [23, 10], [27.6, 11.6]], PAL.creme), a2 = C.arrow([[19, 3.5], [25, 3.2], [31, 6.5]], PAL.ouro), a3 = C.arrow([[28, 11.6], [30, 9], [31, 6.8]], PAL.creme);
const zone = C.zone(30.5, 6, 4.2), goalZ = C.zone(39, 12, 3.2, PAL.ouro);
// keyframed camera
const K = [[0, { x: 21, z: 12, az: 0, el: 1.2, d: 104 }], [4.8, { x: 21, z: 12, az: 0, el: 1.16, d: 98 }], [7.6, { x: 25, z: 10, az: -.32, el: 1.08, d: 70 }],
           [10.4, { x: 27, z: 9, az: -.38, el: 1.05, d: 64 }], [13.2, { x: 33, z: 9, az: -1.05, el: .72, d: 50 }], [14.6, { x: 33, z: 9, az: -1.08, el: .7, d: 48 }], [17.2, { x: 21, z: 12, az: 0, el: 1.2, d: 104 }], [18, { x: 21, z: 12, az: 0, el: 1.2, d: 106 }]];
const camAt = (t) => { let k = 0; while (k < K.length - 2 && t > K[k + 1][0]) k++; const [t0, a] = K[k], [t1, b] = K[k + 1], p = eio(seg(t, t0, t1)); const o = {}; for (const key in a) o[key] = lerp(a[key], b[key], p); return o; };
[[4.8, 2.8], [10.4, 2.8], [14.6, 2.6]].forEach(([t, d]) => ev(t, 'whoosh', { d }));
// the move: 5 → 9 (5.6), 7 runs into the space (6.2–8.6), 9 → 7 (8.7), 7 finishes (11.4)
ev(5.6, 'kick'); ev(8.7, 'kick'); ev(11.4, 'kick', { v: 1.4 }); ev(12.15, 'goal'); ev(12.15, 'net');
window.DUR = 18; window.EV = EV.sort((a, b) => a.t - b.t);
const pos = (p0, p1, p) => [lerp(p0[0], p1[0], p), lerp(p0[1], p1[1], p)];
window.render = (t) => {
  const v = camAt(t), az = C.view(v);
  // drop in, then the move
  A.forEach(([n, x, z], i) => { const d = seg(t, drop(i, 0), drop(i, 0) + .45); TA[i].at(x, z, (1 - eo(d)) * 7, d > 0 ? 1 : 0); });
  B.forEach(([n, x, z], i) => { const d = seg(t, drop(i, 1), drop(i, 1) + .45); TB[i].at(x, z, (1 - eo(d)) * 7, d > 0 ? 1 : 0); });
  const run7 = eio(seg(t, 6.2, 8.6)), p7 = pos([19, 3.5], [31, 6.5], run7); TA[4].at(...p7);
  const p9 = pos([28, 12], [27.6, 11.6], eio(seg(t, 5.2, 6.4))); TA[6].at(...p9);
  TB[1].at(...pos([31, 8], [29.5, 10.5], eio(seg(t, 5.8, 7)))); // their 4 is pulled to the 9
  // ball
  let b;
  if (t < 5.6) b = [18 + 1.3, 12, 0]; else if (t < 6.5) { const p = eo(seg(t, 5.6, 6.5)); b = [...pos([19.3, 12], [26.4, 11.6], p), Math.sin(p * Math.PI) * 1.2]; }
  else if (t < 8.7) b = [26.4, 11.6, 0]; else if (t < 9.6) { const p = eo(seg(t, 8.7, 9.6)); b = [...pos([27, 11], [30.2, 7.6], p), 0]; }
  else if (t < 11.4) b = [30.2 + 1.2 * seg(t, 9.6, 11.4), 7.6 - .4 * seg(t, 9.6, 11.4), 0]; else { const p = eo(seg(t, 11.4, 12.15)); b = [...pos([31.4, 7.2], [39.6, 11], p), Math.sin(p * Math.PI) * .9 + p * .6]; }
  C.ball.at(...b);
  bars.forEach((g, i) => g.show(seg(t, BAR_T[i], BAR_T[i] + .3) * (1 - seg(t, 5.0, 5.5))));
  a1.reveal(seg(t, 5.0, 5.6)); a2.reveal(seg(t, 5.9, 6.5)); a3.reveal(seg(t, 8.3, 8.7));
  zone.show(seg(t, 6.4, 6.9) * (1 - seg(t, 10.6, 11))); goalZ.show(seg(t, 12.15, 12.3) * (1 - seg(t, 13.6, 14.4)) * (1 + .3 * Math.sin(t * 18)));
  C.render();
  // channel layer
  const tt = seg(t, .5, .9), gp = seg(t, 12.15, 12.45), out = t > 15.2, ep = seg(t, 15.4, 15.9);
  const labs = [['2', 2.5, 1300], ['3', 3.1, 1040], ['1', 3.7, 820]].map(([s, t0, y]) => { const p = seg(t, t0, t0 + .3) * (1 - seg(t, 5.0, 5.3)); return p > 0 ? `<div class="lab" style="right:200px;top:${y}px;opacity:${p};transform:scale(${.6 + .4 * back(p)})">${s}</div>` : ''; }).join('');
  ui.innerHTML = `<img class="logo" src="logo.png"><div class="tag" style="opacity:${tt}">PRANCHETA Nº 1 · SOCIETY</div>`
   + (!out ? `<div class="title" style="opacity:${tt * (1 - seg(t, 4.8, 5.2))};transform:translateY(${(1 - eo(tt)) * 30}px)"><div style="width:${380*tt}px;height:2px;background:#D4A537;margin:0 0 14px 4px"></div><div style="font-size:84px">ESSE É O</div><div style="font-size:196px;color:#D4A537">2-3-1</div></div>` : '')
   + labs
   + (gp > 0 && t < 14.6 ? `<div class="pop" style="top:560px;font-size:${300 * (.7 + .3 * back(gp))}px;opacity:${1 - seg(t, 14, 14.6)}">GOL</div>` : '')
   + (ep > 0 ? `<div style="position:absolute;inset:0;background:rgba(17,17,17,${.72 * ep})"></div><div class="pop" style="top:560px;font-size:150px;color:#F2E9D8;opacity:${ep}">2 ATRÁS<br>3 NO MEIO<br><span style="color:#D4A537">1 NA FRENTE</span></div>` : '');
};
ev(.5, 'print'); ev(12.15, 'stamp'); ev(15.4, 'print');
window.READY = true;
