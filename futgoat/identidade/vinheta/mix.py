"""Sound sting for the Futgoat vinheta (1.2 s): low thump, gold shimmer and a two-note chime. Usage: python mix.py out.wav"""
import os, sys
import numpy as np, soundfile as sf
LIB = os.environ.get('LIB') or '/home/user/lemo-opuscar'
sys.path.insert(0, LIB)
from core.audio.sfx import SR, bp, lp, hp, add, limit, thump, whoosh
N = int(1.2 * SR); rng = np.random.default_rng(9); buf = np.zeros((N, 2))
def tt(d): return np.arange(int(d * SR)) / SR
def bell(f, d=1.2, v=1.0):
    t = tt(d); x = sum(np.sin(2 * np.pi * f * k * t) * np.exp(-t * (2.2 + 1.8 * k)) / k for k in (1, 2, 3.01, 4.2)); return x * v * .3
add(buf, whoosh(.45, 1.0) * .22, .0, 1, 0)
add(buf, thump(v=1.0, f=60)[:int(.5 * SR)] * .9, .13, 1, 0)
add(buf, bp(rng.standard_normal(int(.5 * SR)), 5000, 11000) * np.exp(-tt(.5) / .18) * .09, .5, 1, .3)
add(buf, bell(784, 0.9, 1.0), .52, 1, -.2); add(buf, bell(1175, 0.8, .8), .6, 1, .2)
fade = np.ones(N); i0 = int(0.9 * SR); fade[i0:] = np.linspace(1, 0, N - i0); buf *= fade[:, None]
out = np.stack([limit(buf[:, c], ceil=.85) for c in range(2)], 1); sf.write(sys.argv[1], out.astype(np.float32), SR); print('ok')
