import json, numpy as np, soundfile as sf
from faster_whisper import WhisperModel
a, sr = sf.read('bruto.wav', dtype='float32')
fr = int(.05*sr); e = np.array([np.sqrt(np.mean(a[i:i+fr]**2)) for i in range(0, len(a)-fr, fr)])
print('pico', round(float(np.abs(a).max()),3), '| ruído (10%)', round(float(np.percentile(e,10)),4), '| fala (90%)', round(float(np.percentile(e,90)),4))
a16 = np.interp(np.linspace(0, len(a)-1, int(len(a)*16000/sr)), np.arange(len(a)), a).astype('float32')
m = WhisperModel('small', device='cpu', compute_type='int8')
segs, _ = m.transcribe(a16, language='pt', word_timestamps=True, vad_filter=False)
out = [{"s": round(s.start,2), "e": round(s.end,2), "t": s.text.strip(), "w": [{"w": w.word.strip(), "s": round(w.start,2), "e": round(w.end,2)} for w in s.words]} for s in segs]
json.dump(out, open('trans.json','w'), ensure_ascii=False, indent=1)
for s in out: print(f"{s['s']:6.1f}-{s['e']:6.1f} {s['t']}")
