"""Indexa um mp3 do ElevenLabs (já transcrito pelo Whisper) em banco por frase/palavra.
Uso: python construir_eleven.py trans.json voz.mp3-ou-wav saida_dir [texto_esperado.json bloco,bloco...]
Corrige as palavras que o Whisper ouviu errado usando o texto esperado (alinhamento por difflib)."""
import json, os, re, sys, difflib, subprocess, unicodedata
import numpy as np, soundfile as sf
from num2words import num2words
SR = 44100
def norm(w):
    w = unicodedata.normalize("NFC", w.lower()); return re.sub(r"[^\wà-ú-]", "", w).strip("-")
def toks(t):
    t = re.sub(r"\d+", lambda m: num2words(int(m.group()), lang="pt_BR"), t)
    return [x for x in (norm(w) for w in t.split()) if x]
trans, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
esp = []
if len(sys.argv) > 5:
    bl = json.load(open(sys.argv[4]))["blocos"]
    for b in sys.argv[5].split(","): esp += [w for f in bl[b] for w in toks(f)]
os.makedirs(out + "/audio", exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ar", str(SR), "-ac", "1", out + "/_full.wav"], check=True)
a, _ = sf.read(out + "/_full.wav")
segs = json.load(open(trans))
heard = []; ref = []
for si, s in enumerate(segs):
    for w in s["w"]:
        for t in toks(w["w"]) or []: heard.append(t); ref.append((si, w))
fixed = list(heard)
if esp:
    sm = difflib.SequenceMatcher(None, heard, esp, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "replace" and i2 - i1 == j2 - j1: fixed[i1:i2] = esp[j1:j2]
    print("palavras corrigidas:", sum(1 for x, y in zip(heard, fixed) if x != y), "de", len(heard))
idx = {"sr": SR, "frases": {}}; k = 0
for si, s in enumerate(segs):
    ws = []; t0 = max(0, s["s"] - 0.15)
    for w in s["w"]:
        n = len(toks(w["w"]))
        if not n: continue
        parts = fixed[k:k + n]; k += n; d = (w["e"] - w["s"]) / n
        for q, p in enumerate(parts): ws.append({"w": p, "s": round(w["s"] + q * d - t0, 3), "e": round(w["s"] + (q + 1) * d - t0, 3)})
    if not ws: continue
    t1 = min(len(a) / SR, s["e"] + 0.15)
    fid = "f%03d" % (si + 1)
    sf.write(f"{out}/audio/{fid}.wav", a[int(t0 * SR):int(t1 * SR)], SR)
    idx["frases"][fid] = {"texto": " ".join(w["w"] for w in ws), "ratio": 1.0, "ok": True, "dur": round(t1 - t0, 3), "palavras": ws}
json.dump(idx, open(out + "/index.json", "w"), ensure_ascii=False, indent=1)
print(out, len(idx["frases"]), "frases")
