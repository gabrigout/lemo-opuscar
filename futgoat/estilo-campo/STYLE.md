# Futgoat Pitch 3D · Futgoat 3D 球场 — Style Prompt

Made from a blank page; techniques from Isometric Infographic (iso-infographic) in Lemo-Opuscar, with moves borrowed from Sports Telestrator (telestrator) and Projection-Mapped Model (white-model).
Default size: 1080×1920 (vertical), 30 fps.

> Football tactics on a tilted 3D pitch: players are numbered discs, the ball is a small cream sphere, runs and passes are dashed arrows painted on the turf, and the space that matters glows. A big condensed title and a series tag sit on top; the camera starts wide on the formation and pushes into the move. The channel's look (Futgoat) is the palette and the type, not a broadcast.

## 1. Essence, and what it is not
- **The pitch is the stage.** A real-proportion pitch (society 40×24 m, futsal 40×20, field 105×68) as a dark graphite tactics board with faint stripes and cream lines, tilted towards the viewer, our goal at the bottom, attack up the screen.
- **Players are discs.** A flat cylinder per player with the shirt number on top, one colour per team (ours gold, the opponent cream). No bodies, faces, crests or kits.
- **One idea per move.** Each beat shows one thing: a formation, a pass, a run into space, a finish.
- **The formation reads first.** The opening is always the whole pitch from behind our goal, every line legible.
Not Sports Telestrator (no real footage), not Isometric Infographic (no icons, no orthographic camera), not a video game (no HUD, no players with bodies).

## 2. Materials & rendering
- three.js, PBR standard materials, one warm key light from the left-front with soft shadows, a hemisphere fill; no bloom.
- Board: a hi-res canvas texture (100 px per metre) with ten faint graphite stripes (#202125 / #26272B), a 5 m dotted grid at ~10 % cream (a drawing-board detail) and **hairline cream markings, 0.07 m wide**: touchlines, halfway line, centre circle and spot, penalty and goal areas, penalty arcs and spots, corner arcs. The pitch is a slab with a darker apron. Not green: the brand has no green.
- Discs: radius = pitch length / 40, thin (0.36 r), the number in Anton on the top face (512 px texture), a hairline dark rim and a second fine inner ring in the number colour. The ball: cream, radius 0.36 r, casts a shadow.
- Arrows: **hairline** dashes (width 0.075 r) along a Catmull-Rom curve on the board, a small open triangular head, a start dot; cream for the ball's path, gold for a run.
- Zones: a flat circle at 14 % with a hairline ring at 80 % around it (gold). Formation bars: a thin band (0.35 r) through a line of players at 30 %.

## 3. Colour logic
- The Futgoat palette, nothing else: warm black #111111 (background, deepest areas), gold #D4A537 (our team, our runs, the key word, the channel mark), cream #F2E9D8 (the opponent, the pitch lines, titles, the ball and the ball's path), bronze #8A5A12 (shadow shapes, a third team, ridges), graphite #2A2A2E and #3A3A3C (the board, the jacket, a fourth team).
- Gold means "ours / the answer": the team the video is about, the run that matters, the one key word of a subtitle. Cream means "the other one" or a neutral line.
- No green, no pure white, no pure black fills, no club colours: teams are told apart only by gold, cream, bronze and graphite.

## 4. Type & subtitles
- The round Futgoat logo top left (120 px, below the 135 px top UI band). Series tag beside it: gold plate, Anton 34 px, "PRANCHETA Nº 1 · SOCIETY".
- Title top left: Anton, a short line 110 px over the key term 260 px in gold, with a 6 px dark drop.
- Subtitles (when there is a voice): a warm black box with a 4 px gold border, Archivo Black 42 px, the key word in gold, bottom band y ≈ 1340–1480, at most two lines.
- Line labels ("2", "3", "1"): gold plates 200 px in from the right edge (the platforms' buttons live in the last ~180 px), level with each line.
- Every label holds ≥ letters ÷ 15 + 1.5 s.

## 5. Motion quality
- Players enter by dropping onto the pitch (ease-out, staggered 0.12 s, team by team), never by fading.
- Arrows are drawn along their path before the move (0.5 s); the ball travels with an ease-out and a small arc for a lofted pass; runs are eased in and out.
- Big words pop with a back-ease scale; the end card fades the pitch under a warm black veil.
- Never moves: the pitch, the lines, a player who is not in the move.

## 6. Camera grammar
| Move | What it expresses | Can serve |
|---|---|---|
| Wide from behind our goal, high | the shape of the team | a formation, an opening |
| Push and slight turn towards the move | where the play happens | a pass, a run, a space |
| Orbit low to the side | the moment of truth | a shot, a save, an offside line |
| Pull back high to the wide | the lesson | a summary, the end card |
Every move eases in and out; no cuts inside one move.

## 7. Sound palette
- Music: a synthesised modern beat around 108 BPM (kick, snare, hats, a round bass, plucked chords); it drops for one bar before the decisive moment.
- Foley: a soft thud per disc landing, a click per label, a whoosh per camera move, a ball kick (low thump + click), the net, a crowd swell on a goal.
- With a voice: voice ~11 dB over the music, master −14 LUFS, true peak ≤ −1 dB.

## 8. Native moves
- **Drop-in formation**: the discs fall onto the pitch line by line, then gold bars light each line ("2", "3", "1").
- **Arrow first**: the dashed path is painted before the ball or the runner follows it.
- **The space lights up**: a zone glows where the run will arrive, before the player gets there.
- **Orbit to the finish**: the camera swings low to the side for the shot, the goal glows, a big word pops.

## 9. Pitfalls of the medium
- Numbers upside down or sideways: spin the discs to the camera's azimuth every frame (`face(az)`).
- The ball hiding a number: keep the ball off the disc centre (ahead of the player).
- A close camera that loses the formation: open wide first, push only for the move.
- The title over the far goal: keep the key title short and let it leave before the move.
- Too many arrows: at most two at a time.
- Real people: names only in the voice and subtitles; no faces, crests or kits.

## 10. Engine
- `demo/engine/campo.js`: `createCampo(canvas, {W, H, kind})` → `token(n, team).at(x, z, lift, scale)`, `ball.at(x, z, h)`, `arrow(points, colour).reveal(p)`, `zone(x, z, r, colour).show(a)`, `bar(points).show(a)`, `view({x, z, az, el, d})`, `render()`; `PAL`, `TEAM`, `PITCH`.
- `demo/main.js`: the demo (drop-in, bars, the move, the orbit, the end card) and the channel layer in HTML on top. `demo/mix.py`: the beat and the foley from the page's events.
- Technique base: `$LIB/styles/iso-infographic/`.

## 11. Variation space
Pitch kind (society, futsal, field), the teams' colours (within the palette), the series tag, the move, how many camera moves (2–4), whether a presenter appears in his own corner frame, and the voice.

## Line weights (rule)
Lines are always fine: markings 0.07 m, arrows and rims hairline, plates in the channel layer are 1.5 to 2 px outlines, never solid heavy boxes. Detail comes from many fine marks (areas, arcs, grid, rings), not from thick ones.
