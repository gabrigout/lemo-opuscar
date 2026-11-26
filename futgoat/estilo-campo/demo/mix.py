"""Sound for the Futopia · Campo 3D demo: a synthesised 108 BPM beat (kick, snare, hats, bass, plucked chords) and pitch foley.
Inputs: events.json (from the page). Output: $OUT/mix.wav (48 kHz stereo). Usage: python mix.py <events.json> <out.wav>"""
import json, os, sys
import numpy as np, soundfile as sf
LIB = os.environ.get('LIB') or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.insert(0, LIB)
from core.audio.sfx import SR, bp, lp, hp, add, limit, thump, whoosh, click
EV = json.load(open(sys.argv[1])); DUR = float(EV['dur']); EV = EV['ev']; N = int(DUR * SR)
rng = np.random.default_rng(3); B = 60 / 108; BAR = 4 * B
def nz(d): return rng.standard_normal(max(1, int(d * SR)))
def tt(d): return np.arange(int(d * SR)) / SR
def env(n, a, r): e = np.ones(n); a = min(n, int(a * SR)); r = min(n - a, int(r * SR)); e[:a] = np.linspace(0, 1, a) if a else 1; e[n - r:] = np.linspace(1, 0, r) if r else 1; return e
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def kick(v=1): t = tt(.35); return np.sin(2 * np.pi * np.cumsum(50 + 90 * np.exp(-t / .03)) / SR) * np.exp(-t / .16) * .8 * v
def snare(v=1): t = tt(.25); return (bp(nz(.25), 1200, 6000) * np.exp(-t / .07) * .5 + np.sin(2 * np.pi * 190 * t) * np.exp(-t / .05) * .3) * v
def hat(v=1): d = .05; return hp(nz(d), 7000) * np.exp(-tt(d) / .012) * .22 * v
def bass(f, d, v=1): t = tt(d); x = np.sin(2 * np.pi * f * t) + .3 * np.sign(np.sin(2 * np.pi * f * t)) * .4; return lp(x, 500) * env(len(t), .005, .08) * .45 * v
def pluck(f, v=1): t = tt(.6); x = sum(np.sin(2 * np.pi * f * k * t) / k ** 1.4 * np.exp(-t * (3 + 2 * k)) for k in range(1, 7)); return x * env(len(t), .003, .05) * .22 * v
mus = np.zeros((N, 2))
prog = [(45, [57, 60, 64]), (41, [57, 60, 65]), (36, [55, 60, 64]), (43, [55, 59, 62])]   # Am F C G
for b in range(int(np.ceil(DUR / BAR))):
    t0 = b * BAR; root, ch = prog[b % 4]
    hush = 11.0 < t0 < 12.0
    for k in range(4):
        add(mus, kick(.9), t0 + k * B, 1, 0) if k in (0, 2) or b >= 5 else None
        if k in (1, 3) and t0 >= BAR: add(mus, snare(.7), t0 + k * B, 1, .05)
        for h in (0, .5): add(mus, hat(.8 if h else .5), t0 + (k + h) * B, 1, .4)
    for k in (0, 1.5, 2, 3.5): add(mus, bass(hz(root), B * .45), t0 + k * B, 1, 0)
    for k, n in zip((.5, 1.5, 2.5, 3), ch + [ch[1] + 12]): add(mus, pluck(hz(n + 12), .9), t0 + k * B, 1, -.3 + .2 * (n % 3))
fade = np.ones(N); i0 = int((DUR - 1.2) * SR); fade[i0:] = np.linspace(1, 0, N - i0)
mus *= fade[:, None] * .55
fo = np.zeros((N, 2))
for e in EV:
    t, ty, v = e['t'], e['type'], e.get('v', 1.0)
    if ty == 'land': add(fo, thump(v=.7 * v, f=110)[:int(.2 * SR)] * .5, t, 1, rng.uniform(-.4, .4))
    elif ty == 'pop': add(fo, hp(click(pitch=1.2, v=1), 900) * .25, t, 1, .3)
    elif ty == 'whoosh': d = min(e.get('d', 1), 3); add(fo, lp(whoosh(d, 1), 2400) * .16, t, 1, 0)
    elif ty == 'kick': add(fo, thump(v=.9 * v, f=140)[:int(.12 * SR)] * .6 + 0, t, 1, 0); add(fo, hp(click(pitch=.8, v=1), 1500) * .3 * v, t, 1, 0)
    elif ty == 'net': add(fo, bp(nz(.5), 2000, 7000) * env(int(.5 * SR), .01, .4) * .12, t + .05, 1, .2)
    elif ty == 'goal':
        d = 2.6; n = int(d * SR); crowd = bp(nz(d), 300, 2500) * env(n, .25, 1.6) * (1 + .3 * np.sin(np.linspace(0, 30, n))) * .35
        add(fo, crowd, t, 1, -.3); add(fo, crowd * .9, t + .02, 1, .3)
    elif ty in ('print', 'stamp'): add(fo, thump(v=.6, f=95)[:int(.15 * SR)] * .35, t, 1, -.2)
out = mus + fo
out = np.stack([limit(out[:, c], ceil=.89) for c in range(2)], 1)
sf.write(sys.argv[2], out.astype(np.float32), SR); print('mix', out.shape)
