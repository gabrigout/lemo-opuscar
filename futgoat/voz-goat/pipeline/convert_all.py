import json, time, numpy as np, soundfile as sf, librosa, torch
from chatterbox.vc import ChatterboxVC
a, sr = sf.read('voz_final.wav', dtype='float32')            # 44,1 kHz, a voz limpa e cortada
P = json.load(open('pecas.json'))['pecas']
m = ChatterboxVC.from_pretrained("cpu"); SR = m.sr
out = a.copy(); t00 = time.time()
rms = lambda x: float(np.sqrt(np.mean(x**2))) + 1e-9
for i, p in enumerate(P, 1):
    s0, s1 = int((p['t0']-.04)*sr), int((p['t1']+.04)*sr)
    seg = a[s0:s1]; src = librosa.resample(seg, orig_sr=sr, target_sr=24000); sf.write('vc_pecas/src.wav', src, 24000)
    w = m.generate('vc_pecas/src.wav', target_voice_path='alvo_kokoro_k2.wav').squeeze(0).cpu().numpy()
    w = librosa.resample(w, orig_sr=SR, target_sr=sr); n = len(seg)
    w = np.pad(w, (0, max(0, n-len(w))))[:n]; w = w * rms(seg)/rms(w)
    f = int(.01*sr); w[:f] *= np.linspace(0, 1, f); w[-f:] *= np.linspace(1, 0, f)
    out[s0:s1] = w * 1.0 + seg * 0.0                             # versão A: 100% convertida (o silêncio entre as falas continua o original)
    sf.write(f'vc_pecas/{i:02d}_{p["id"]}.wav', w, sr); print(i, p['id'], round(time.time()-t00), 's', flush=True)
sf.write('voz_kokoro_total.wav', out, sr); print('DONE', round(len(out)/sr, 1), 's', flush=True)
