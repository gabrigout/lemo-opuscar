# Futgoat Pitch 3D — our demo
One example among many. Don't reuse its story, arc, shots, props or timings.

Demo: *Esse é o 2-3-1* (18 s, no voice) · `test.mp4` · source in `demo/`.
Story: the 2-3-1 of society drops onto the pitch line by line, the 5 passes into the 9, the 7 overlaps into the space, the 9 lays it off, the 7 scores; the end card sums it up (2 atrás, 3 no meio, 1 na frente).
Shots: 0–4.8 wide formation (drop-in 0.25–1.9, bars 2.5–3.7) · 4.8–7.6 push and turn · 7.6–10.4 the move · 10.4–13.2 orbit low to the side, the shot at 11.4, GOL at 12.15 · 14.6–17.2 pull back · end card 15.4–18.
Sound: 108 BPM synthesised beat (Am F C G), kick thumps, a crowd swell on the goal.
Build: `sh demo/build.sh` (LIB at the top; writes to $OUT). Files: `engine/campo.js` (pitch, discs, ball, arrows, zones, bars, camera), `main.js` (the demo and the channel layer), `mix.py` (sound).
