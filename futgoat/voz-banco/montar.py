"""Monta uma frase NOVA a partir do banco: reaproveita os trechos mais longos que existem
e gera localmente (James clonado) só o que falta.
Uso: python montar.py "texto novo" saida.wav [--sem-gerar]"""
import json, os, re, sys, unicodedata
import numpy as np, soundfile as sf

D = os.environ.get("BANCO") or os.path.dirname(os.path.abspath(__file__))
FADE = 0.015

def norm(w):
    w = unicodedata.normalize("NFC", w.lower())
    return re.sub(r"[^\wà-ú-]", "", w).strip("-")

def carregar():
    idx = json.load(open(os.path.join(D, "index.json")))
    sr = idx["sr"]; fr = {}
    for fid, f in idx["frases"].items():
        if not f["ok"]: continue
        a, _ = sf.read(os.path.join(D, "audio", fid + ".wav"))
        fr[fid] = (f["palavras"], a)
    return sr, fr

def corte(ws, a, sr, i, j):
    """Trecho das palavras i..j (inclusive); cortes no meio das pausas vizinhas."""
    ini = ws[i]["s"] if i == 0 else (ws[i - 1]["e"] + ws[i]["s"]) / 2
    fim = ws[j]["e"] + 0.05 if j == len(ws) - 1 else (ws[j]["e"] + ws[j + 1]["s"]) / 2
    return a[int(max(ini, 0) * sr): int(fim * sr)]

def melhor_trecho(alvo, p, fr):
    """Maior sequência de palavras a partir de alvo[p] que existe em alguma frase do banco."""
    best = (0, None)
    for fid, (ws, a) in fr.items():
        pal = [w["w"] for w in ws]
        for i in range(len(pal)):
            n = 0
            while p + n < len(alvo) and i + n < len(pal) and pal[i + n] == alvo[p + n]: n += 1
            if n > best[0]: best = (n, (fid, i, i + n - 1))
    return best

def colar(partes, sr):
    f = int(FADE * sr); out = partes[0].copy()
    for b in partes[1:]:
        k = min(f, len(out), len(b))
        if k > 0:
            r = np.linspace(0, 1, k)
            out[-k:] = out[-k:] * (1 - r) + b[:k] * r
            out = np.concatenate([out, b[k:]])
        else: out = np.concatenate([out, b])
    return out

def main():
    texto, saida = sys.argv[1], sys.argv[2]
    gerar = "--sem-gerar" not in sys.argv
    sr, fr = carregar()
    # pausa de pontuação: após , ; : . ? ! entra um respiro
    pals = texto.split()
    alvo = []; pausa = {}
    for w in pals:
        n = norm(w)
        if not n: continue
        alvo.append(n)
        if re.search(r"[.?!]$", w): pausa[len(alvo) - 1] = 0.28
        elif re.search(r"[,:;]$", w): pausa[len(alvo) - 1] = 0.12
    partes, falt, p, plano = [], [], 0, []
    model = None
    while p < len(alvo):
        n, ref = melhor_trecho(alvo, p, fr)
        if n >= 1:
            fid, i, j = ref; ws, a = fr[fid]
            seg = corte(ws, a, sr, i, j)
            plano.append(("banco", " ".join(alvo[p:p + n]), fid))
        else:
            if not gerar:
                falt.append(alvo[p]); p += 1; continue
            if model is None:
                from chatterbox.mtl_tts import ChatterboxMultilingualTTS
                model = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
            # gera o trecho faltante junto com as palavras seguintes que também faltam
            fim = p + 1
            while fim < len(alvo) and melhor_trecho(alvo, fim, fr)[0] == 0 and fim - p < 6: fim += 1
            txt = " ".join(alvo[p:fim]) + "."
            w = model.generate(txt, language_id="pt", audio_prompt_path=os.path.join(D, "ref_james_12s.wav"), exaggeration=0.5, cfg_weight=0.3)
            seg = w.squeeze(0).cpu().numpy()
            if model.sr != sr:
                import torch, torchaudio as ta
                seg = ta.functional.resample(torch.tensor(seg).unsqueeze(0), model.sr, sr)[0].numpy()
            plano.append(("gerado", " ".join(alvo[p:fim]), "-")); n = fim - p
        partes.append(seg)
        fimp = p + n - 1
        if fimp in pausa: partes.append(np.zeros(int(pausa[fimp] * sr)))
        p += n
    if not partes: sys.exit("nada para montar: " + str(falt))
    out = colar(partes, sr)
    pico = np.abs(out).max()
    if pico > 0: out = out / pico * 0.89
    sf.write(saida, out, sr)
    print("duração %.1fs" % (len(out) / sr))
    for t in plano: print(" ", *t)
    if falt: print("FALTANDO (use sem --sem-gerar):", falt)

if __name__ == "__main__": main()
