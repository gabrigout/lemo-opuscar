"""Gera o banco de voz (James clonado, Chatterbox local) e indexa cada palavra com Whisper.
Uso: python gerar_banco.py   (retoma de onde parou)"""
import json, os, re, sys, unicodedata, difflib
import numpy as np, soundfile as sf, torch, torchaudio as ta
from num2words import num2words
from faster_whisper import WhisperModel
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

D = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(D, "ref_james_12s.wav")
IDX = os.path.join(D, "index.json")

def norm(w):
    w = unicodedata.normalize("NFC", w.lower())
    return re.sub(r"[^\wà-ú-]", "", w).strip("-")

def toks(t):
    t = re.sub(r"\d+", lambda m: num2words(int(m.group()), lang="pt_BR"), t)
    return [x for x in (norm(w) for w in t.split()) if x]

def main():
    frases = json.load(open(os.path.join(D, "vocabulario.json")))["frases"]
    idx = json.load(open(IDX)) if os.path.exists(IDX) else {"sr": 24000, "frases": {}}
    model = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
    asr = WhisperModel("small", device="cpu", compute_type="int8")
    for i, txt in enumerate(frases):
        fid = "f%03d" % (i + 1)
        if fid in idx["frases"]: continue
        best = None
        for tent in range(3):
            wav = model.generate(txt, language_id="pt", audio_prompt_path=REF, exaggeration=0.5, cfg_weight=0.3)
            a = wav.squeeze(0).cpu()
            a16 = ta.functional.resample(a.unsqueeze(0), model.sr, 16000)[0].numpy()
            segs, _ = asr.transcribe(a16, language="pt", word_timestamps=True)
            ws = []
            for sg in segs:
                for x in sg.words:
                    ts = toks(x.word)  # dígitos viram palavras por extenso
                    for k, t in enumerate(ts):
                        d = (x.end - x.start) / len(ts)
                        ws.append({"w": t, "s": round(x.start + k * d, 3), "e": round(x.start + (k + 1) * d, 3)})
            ratio = difflib.SequenceMatcher(None, toks(txt), [w["w"] for w in ws]).ratio()
            print(fid, "tent", tent + 1, "ratio %.2f" % ratio, flush=True)
            if best is None or ratio > best[0]: best = (ratio, a, ws)
            if ratio >= 0.93: break
        ratio, a, ws = best
        sf.write(os.path.join(D, "audio", fid + ".wav"), a.numpy(), model.sr)
        idx["sr"] = model.sr
        idx["frases"][fid] = {"texto": txt, "ratio": round(ratio, 3), "ok": ratio >= 0.9, "dur": round(len(a) / model.sr, 3), "palavras": ws}
        json.dump(idx, open(IDX, "w"), ensure_ascii=False, indent=1)
    print("BANCO PRONTO", len(idx["frases"]), "frases", flush=True)

if __name__ == "__main__": main()
