import json, numpy as np, soundfile as sf
a, sr = sf.read('limpo.wav', dtype='float32')
d = json.load(open('trans.json'))
def W(i): return d[i]['w']
def edge(t0, t1, thr=0.012, pad0=.07, pad1=.12):
    """ajusta o início e o fim para a voz de verdade (energia), com uma folga pequena"""
    fr = int(.01*sr); i0, i1 = int(t0*sr), int(t1*sr)
    e = np.array([np.sqrt(np.mean(a[i:i+fr]**2)) for i in range(i0, i1-fr, fr)])
    v = np.where(e > thr)[0]
    if len(v) == 0: return t0, t1
    return max(0, t0 + v[0]*.01 - pad0), min(len(a)/sr, t0 + v[-1]*.01 + .01 + pad1)
def valley(lo, hi):
    fr = int(.03*sr); best = min(range(int(lo*sr), int(hi*sr)-fr, int(.005*sr)), key=lambda i: np.sqrt(np.mean(a[i:i+fr]**2)))
    return (best + fr//2)/sr
V1, V2, V3 = valley(23.6, 24.0), valley(45.7, 46.1), valley(147.0, 147.7)
print('cortes nos vales:', round(V1, 3), round(V2, 3), round(V3, 3))
# (id, início, fim, legenda, pausa depois)
P = [
 ("gancho", 5.95, 13.62, "O Inter de hoje tá sofrendo no Brasileirão, mas o Internacional de 2006 fez o Barcelona sofrer numa final de Mundial.", .75),
 ("pergunta", 13.78, 20.12, "Agora me diz, como um time vence o Barcelona sem ter a bola? Um plano que é dividido em três fases.", .5),
 ("fase1", 20.35, V1, "A primeira fase, deixar o Barcelona com a bola. Parece loucura, né?", .4),
 ("fase2", V1, 31.95, "A segunda fase, o desenho do time, um 4-4-2 com Pato e Iarley lá na frente. Prontos pra armar o contra-ataque.", .4),
 ("fase3", 32.0, 38.22, "E a terceira fase, a marcação. Sem a bola, Fernandão ficava pertinho do volante Thiago Motta.", .35),
 ("soltos", 40.85, V2, "E o Pato e o Iarley soltos lá na frente, esperando a hora de sair no contra-ataque.", 0.0),
 ("placar", V2, 58.75, "No fim, 1 a 0, gol do Adriano Gabiru no segundo tempo, chocando o mundo do futebol que na época não esperava de nenhuma forma o Internacional vencer o grande Barcelona.", .5),
 ("gente", 59.0, 71.2, "E tinha gente naquele estádio de Yokohama, seis, sete mil pessoas, atônitas, loucas, vendo um time mais forte do mundo no momento perder para um time sul-americano.", .45),
 ("titulo", 76.55, 80.2, "E aí, garantiu o primeiro título mundial em cima do Barcelona.", .6),
 ("licao", 80.65, 84.6, "Um time que aprendeu a sofrer sem a bola e a atacar muito rápido.", .55),
 ("grito", 90.38, 95.1, "O torcedor pede: joga como nunca, Inter, espanta esse fantasma da Série B.", .9),
 ("atual", 103.95, 109.25, "A situação atual do Inter, com 38 pontos na 18ª colocação.", .4),
 ("ultimo", 109.4, 113.75, "O último jogo, perdeu de 5 a 2 pro Vitória, dentro de casa.", .4),
 ("jogos", 114.55, 121.85, "O Internacional ainda joga contra o Bragantino, no Beira-Rio, no dia 29/11, e contra o Cruzeiro, no Mineirão.", .4),
 ("pontos44", 132.95, 136.85, "Ganhando os dois jogos, o Inter fecha com 44 pontos.", .4),
 ("risco", 143.2, V3, "A chance de ser rebaixado é de 93%.", .6),
 ("final", V3, 155.0, "E aí, torcedor, acha que o Inter consegue se inspirar nos dias áureos e consegue se livrar do rebaixamento?", .9),
]
# room tone: a janela mais quieta da gravação
fr = int(.25*sr); qs = min(range(0, len(a)-fr, int(.05*sr)), key=lambda i: np.sqrt(np.mean(a[i:i+fr]**2))); room = a[qs:qs+fr]
rt = lambda n: np.resize(room, n).astype('float32') * .8
parts, tl, t = [rt(int(.4*sr))], [], .4
for k, (pid, t0, t1, leg, pause) in enumerate(P):
    s0, s1 = edge(t0, t1); seg = a[int(s0*sr):int(s1*sr)].copy(); n = int(.012*sr)
    seg[:n] *= np.linspace(0, 1, n); seg[-n:] *= np.linspace(1, 0, n)
    dur = len(seg)/sr; ws = leg.split(); L = [len(w)+2 for w in ws]; tot = sum(L); x = t; words = []
    for w, l in zip(ws, L): dd = dur*l/tot; words.append({"t": w.upper(), "s": round(x, 3), "e": round(x+dd, 3)}); x += dd
    tl.append({"id": pid, "t0": round(t, 3), "t1": round(t+dur, 3), "text": leg, "w": words})
    parts += [seg, rt(int(pause*sr))]; t += dur + pause
parts.append(rt(int(.6*sr))); out = np.concatenate(parts)
sf.write('voz_cortada.wav', out, sr); json.dump({"dur": round(len(out)/sr, 2), "pecas": tl}, open('pecas.json', 'w'), ensure_ascii=False, indent=1)
print('duração', round(len(out)/sr, 1), 's |', len(P), 'peças')
for p in tl: print(f"{p['t0']:6.1f} {p['t1']:6.1f} {p['id']}")
