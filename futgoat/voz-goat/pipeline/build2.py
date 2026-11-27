import json, numpy as np, soundfile as sf, subprocess, os
D = os.path.dirname(os.path.abspath(__file__)); FF = os.environ["FFMPEG"]
subprocess.run([FF, "-v", "error", "-y", "-i", f"{D}/voz_kokoro_total.wav", "-af", "loudnorm=I=-16:TP=-1.5:LRA=7", "-ar", "44100", f"{D}/voz_k_norm.wav"], check=True)
voz, SR = sf.read(f"{D}/voz_k_norm.wav", dtype="float32")
TL = json.load(open(f"{D}/pecas.json")); P = {p["id"]: p for p in TL["pecas"]}
DUR = round(len(voz)/SR + .4, 2); N = int(DUR*SR); voz = np.pad(voz, (0, N-len(voz)))
tt = np.arange(N)/SR; beat = 60/96; bed = np.zeros(N, dtype="float32")
for k in range(int(DUR/beat)+1):
    i0 = int(k*beat*SR); n = int(.22*SR); e = np.exp(-np.arange(n)/SR*20)
    kick = np.sin(2*np.pi*(52+95*np.exp(-np.arange(n)/SR*42))*np.arange(n)/SR)*e
    if i0+n < N: bed[i0:i0+n] += .5*kick
    j0 = int((k+.5)*beat*SR); m = int(.045*SR)
    if j0+m < N: bed[j0:j0+m] += .07*np.random.RandomState(k).randn(m)*np.exp(-np.arange(m)/SR*100)
roots = [55, 55, 41.2, 49]
for k in range(int(DUR/(4*beat))+1):
    i0 = int(k*4*beat*SR); n = int(4*beat*SR); f0 = roots[k % 4]; seg = np.arange(min(n, N-i0))
    if len(seg): bed[i0:i0+len(seg)] += .15*np.sin(2*np.pi*f0*seg/SR)*np.minimum(1, seg/2000)*np.exp(-seg/SR*.6)
env = np.convolve(np.abs(voz), np.ones(2205)/2205, "same"); env = env/env.max()
bed *= (1 - .6*np.clip(env*3, 0, 1)); bed *= np.minimum(1, tt/1.5)*np.minimum(1, (DUR-tt)/1.2)
sfx = np.zeros(N, dtype="float32")
def whoosh(t0, d=.5, a=.18, seed=0):
    n = int(d*SR); i = int(t0*SR); x = np.convolve(np.random.RandomState(seed).randn(n), np.ones(30)/30, "same")*np.sin(np.linspace(0, np.pi, n))**2; sfx[i:i+n] += a*x[:max(0, N-i)][:n]
def hit(t0, a=.5):
    n = int(.6*SR); i = int(t0*SR); s = np.arange(n)/SR; x = (np.sin(2*np.pi*70*s)+.4*np.random.RandomState(9).randn(n)*np.exp(-s*30))*np.exp(-s*7); sfx[i:i+n] += a*x[:max(0, N-i)][:n]
def ding(t0, a=.12):
    n = int(1.8*SR); i = int(t0*SR); s = np.arange(n)/SR; x = (np.sin(2*np.pi*988*s)+.5*np.sin(2*np.pi*1482*s))*np.exp(-s*2.2); sfx[i:i+n] += a*x[:max(0, N-i)][:n]
for k, pid in enumerate(["pergunta", "placar", "gente", "grito", "atual", "final"]): whoosh(P[pid]["t0"]-.38, seed=k)
hit(P["placar"]["t0"]+.1); hit(P["gente"]["t0"]+.1, .35); hit(P["grito"]["t0"]+.05, .45); ding(P["titulo"]["t0"]+.05); hit(P["risco"]["t0"]+.2, .4)
mix = voz + bed*.22 + sfx*.6; mix = mix/np.abs(mix).max()*.9
sf.write(f"{D}/page/mix.wav", mix, SR)
FPS = 30; hop = SR//FPS; NF = int(DUR*FPS)+1
rms = np.array([float(np.sqrt(np.mean(voz[i*hop:(i+1)*hop+hop//2]**2))) if i*hop < N else 0 for i in range(NF)])
ref = np.percentile(rms[rms > .01], 75); mouth = [0 if r < .012 else (1 if r < ref*.5 else 2) for r in rms]
for i in range(1, NF-1):
    if mouth[i-1] == mouth[i+1] != mouth[i]: mouth[i] = mouth[i-1]
json.dump({"dur": DUR, "fps": FPS, "pecas": TL["pecas"], "mouth": mouth, "blinks": [2.4, 7.0, 13.5, 21.0, 29.5, 38.0, 47.0, 58.0, 68.0, 78.0, 89.0, 100.0, 110.0]}, open(f"{D}/page/timeline.json", "w"), ensure_ascii=False)
print("DUR", DUR)
