"""Fundos originais do Futgoat, desenhados em código (sem foto, sem pessoa, sem escudo).
Paleta: #111111, #2A2A2E, #D4A537 (dourado), #8A5A12 (bronze), #F2E9D8 (creme).
Uso: python gerar_fundos.py  -> gera 49 JPGs 1080x1920 em fundos/"""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter

W, H, S = 1080, 1920, 2           # desenha em 2x e reduz (linhas finas nítidas)
OURO, BRONZE, CREME = (212, 165, 55), (138, 90, 18), (242, 233, 216)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fundos")

def base(seed):
    rnd = random.Random(seed)
    img = Image.new("RGB", (W * S, H * S), (17, 17, 17))
    px = img.load()
    cx, cy = (W * S) * (0.5 + rnd.uniform(-0.1, 0.1)), (H * S) * (0.38 + rnd.uniform(-0.05, 0.05))
    for y in range(0, H * S, 4):
        for x in range(0, W * S, 4):
            d = math.hypot((x - cx) / (W * S), (y - cy) / (H * S))
            t = max(0.0, 1 - d * 1.6)
            c = tuple(int(17 + (42 - 17) * t + g * 0.18 * t * t) for g in (0, 0, 0))
            c = (int(c[0] + 0.0), int(c[1] + 0.0), int(c[2] + 0.0))
            col = (int(17 + (42 - 17) * t + 212 * 0.10 * t * t), int(17 + (42 - 17) * t + 165 * 0.10 * t * t), int(17 + (46 - 17) * t + 55 * 0.06 * t * t))
            for dy in range(4):
                for dx in range(4):
                    if x + dx < W * S and y + dy < H * S:
                        px[x + dx, y + dy] = col
    return img

def line(d, p, q, col=OURO, w=2, a=255):
    d.line([(p[0] * S, p[1] * S), (q[0] * S, q[1] * S)], fill=col + (a,), width=w * S)

def rect(d, x, y, w, h, col=OURO, lw=2, a=255):
    d.rectangle([x * S, y * S, (x + w) * S, (y + h) * S], outline=col + (a,), width=lw * S)

def circ(d, x, y, r, col=OURO, lw=2, a=255):
    d.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], outline=col + (a,), width=lw * S)

def finish(img, layer, name):
    img = img.convert("RGBA")
    layer = layer.resize((W, H), Image.LANCZOS)
    out = Image.alpha_composite(img.resize((W, H), Image.LANCZOS), layer).convert("RGB")
    vig = Image.new("L", (W, H), 0); vd = ImageDraw.Draw(vig)
    vd.ellipse([-W * 0.3, -H * 0.1, W * 1.3, H * 1.1], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(160))
    dark = Image.new("RGB", (W, H), (10, 10, 10))
    out = Image.composite(out, dark, vig.point(lambda v: int(255 * (0.55 + 0.45 * v / 255))))
    out.save(os.path.join(OUT, name), quality=88)

def layer():
    return Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))

# ---------- motivos ----------
def campo(d, rnd):           # linhas de campo em perspectiva
    rect(d, 120, 560, 840, 1000, a=150, lw=2)
    line(d, (120, 1060), (960, 1060), a=150); circ(d, 540, 1060, 110, a=150)
    rect(d, 300, 560, 480, 170, a=120); rect(d, 380, 560, 320, 70, a=120)
    rect(d, 300, 1390, 480, 170, a=120); rect(d, 380, 1490, 320, 70, a=120)

def setas(d, rnd):
    for i in range(4):
        y = 700 + i * 180 + rnd.randint(-20, 20)
        line(d, (200, y), (880, y + rnd.randint(-80, 80)), a=110)
        x, yy = 880, y
        line(d, (x, yy), (x - 24, yy - 14), a=110); line(d, (x, yy), (x - 24, yy + 14), a=110)

def circulos(d, rnd):
    for i in range(6):
        circ(d, rnd.randint(150, 930), rnd.randint(500, 1400), rnd.randint(40, 140), a=rnd.randint(70, 150))

def pontos(d, rnd):
    for j in range(5):
        for i in range(8):
            x, y = 160 + i * 110, 560 + j * 200
            circ(d, x, y, 4, lw=2, a=160)

def lousa(d, rnd):
    rect(d, 150, 600, 780, 760, a=140, lw=3)
    line(d, (180, 680), (900, 680), a=90); line(d, (180, 1280), (900, 1280), a=90)
    for k in range(3):
        line(d, (260 + k * 230, 760), (260 + k * 230, 1200), a=70)

def tunel(d, rnd):
    rect(d, 380, 720, 320, 480, a=140, lw=2)
    rect(d, 330, 670, 420, 580, a=90, lw=2)
    line(d, (330, 670), (380, 720), a=80); line(d, (750, 670), (700, 720), a=80)
    line(d, (330, 1250), (380, 1200), a=80); line(d, (750, 1250), (700, 1200), a=80)

def arquibancada(d, rnd):
    for k in range(7):
        r = 260 + k * 110
        for ang in range(200, 341, 4):
            a = math.radians(ang)
            x, y = 540 + r * math.cos(a) * 1.15, 1250 + r * math.sin(a) * 0.9
            if 60 < x < 1020 and 300 < y < 1800:
                d.ellipse([x * S - 2, y * S - 2, x * S + 2, y * S + 2], fill=OURO + (110,))

def refletor(d, rnd):
    for k, x in enumerate([200, 540, 880]):
        rect(d, x - 60, 480, 120, 90, a=160)
        for i in range(4):
            for j in range(3):
                line(d, (x - 46 + i * 30, 492 + j * 26), (x - 46 + i * 30 + 16, 492 + j * 26), a=120, w=2)
        line(d, (x, 570), (x, 760), a=100)

def cartaz(d, rnd):
    rect(d, 220, 560, 640, 880, a=150, lw=3)
    rect(d, 250, 600, 580, 800, a=80, lw=1)
    line(d, (300, 700), (780, 700), a=110); line(d, (300, 780), (700, 780), a=80)
    circ(d, 540, 1000, 120, a=110)

def trofeu_mold(d, x, y, s=1.0, a=170):
    circ(d, x, y, 90 * s, a=a)
    line(d, (x - 40 * s, y + 90 * s), (x + 40 * s, y + 90 * s), a=a)
    line(d, (x, y + 90 * s), (x, y + 150 * s), a=a)
    rect(d, x - 70 * s, y + 150 * s, 140 * s, 40 * s, a=a)

def sala_trofeus(d, rnd):
    for i in range(3):
        y = 760 + i * 300
        line(d, (150, y + 160), (930, y + 160), a=140)
        for k in range(4):
            trofeu_mold(d, 260 + k * 190, y + 10, s=0.5 + 0.1 * (k % 2), a=130)

def bola(d, rnd):
    circ(d, 540, 960, 250, lw=3, a=160)
    for k in range(5):
        a = math.radians(-90 + k * 72)
        x, y = 540 + 250 * 0.45 * math.cos(a), 960 + 250 * 0.45 * math.sin(a)
        line(d, (540, 960), (x, y), a=110)

def coroa(d, rnd):
    for k in range(9):
        t = math.radians(200 + k * 20)
        x, y = 540 + 280 * math.cos(t), 960 + 280 * math.sin(t) * 0.8
        circ(d, x, y, 36, a=110)

def balanca(d, rnd):
    line(d, (540, 620), (540, 1300), a=140)
    line(d, (240, 720), (840, 720), a=140)
    line(d, (240, 720), (180, 980), a=100); line(d, (240, 720), (300, 980), a=100)
    line(d, (840, 720), (780, 980), a=100); line(d, (840, 720), (900, 980), a=100)
    rect(d, 150, 980, 180, 40, a=110); rect(d, 750, 980, 180, 40, a=110)

def martelo(d, rnd):
    rect(d, 380, 1000, 320, 180, a=130, lw=3)
    line(d, (360, 1000), (720, 1000), a=140, w=3)
    rect(d, 500, 660, 80, 340, a=130, lw=3)

def dois_lados(d, rnd):
    line(d, (540, 520), (540, 1400), a=130)
    for k in range(5):
        rect(d, 160 + 40 * k, 600 + k * 120, 340 - 40 * k, 40, a=90 + 20 * k)
        rect(d, 580 + 40 * (4 - k), 600 + k * 120, 340 - 40 * (4 - k), 40, a=90 + 20 * (4 - k))

def microfone(d, rnd):
    rect(d, 470, 700, 140, 220, a=150, lw=3)
    circ(d, 540, 700, 70, a=120)
    line(d, (540, 920), (540, 1150), a=130)
    line(d, (420, 1150), (660, 1150), a=130)

def votacao(d, rnd):
    for k in range(6):
        h = 80 + rnd.randint(40, 260)
        rect(d, 200 + k * 130, 1300 - h, 80, h, a=140)
    line(d, (160, 1300), (920, 1300), a=120)

def spot(d, rnd):
    rect(d, 150, 600, 780, 500, a=90)
    for i in range(3):
        circ(d, 540, 1000, 120 + i * 80, a=70 + i * 40)

def caixa(d, rnd):
    rect(d, 260, 760, 560, 380, a=150, lw=3)
    rect(d, 260, 700, 560, 60, a=120, lw=2)
    line(d, (540, 700), (540, 760), a=120)

def cofre(d, rnd):
    circ(d, 540, 960, 300, lw=3, a=150)
    circ(d, 540, 960, 200, a=110)
    for k in range(12):
        t = math.radians(k * 30)
        line(d, (540 + 200 * math.cos(t), 960 + 200 * math.sin(t)), (540 + 240 * math.cos(t), 960 + 240 * math.sin(t)), a=120)
    line(d, (540, 960), (640, 860), a=150)

def lupa(d, rnd):
    circ(d, 500, 900, 180, lw=3, a=150)
    line(d, (640, 1040), (860, 1260), a=150, w=4)

def livro(d, rnd):
    line(d, (540, 620), (540, 1300), a=120)
    for k in range(8):
        line(d, (200, 680 + k * 70), (500, 680 + k * 70 - 20), a=90)
        line(d, (580, 680 + k * 70 - 20), (880, 680 + k * 70), a=90)

def raio_x(d, rnd):
    for k in range(5):
        circ(d, 540, 960, 80 + k * 60, a=90 + k * 10)
    line(d, (100, 960), (980, 960), a=70)

def ficha(d, rnd):
    rect(d, 220, 640, 640, 620, a=140, lw=3)
    line(d, (280, 720), (800, 720), a=110)
    for k in range(4):
        line(d, (280, 800 + k * 80), (760 - k * 60, 800 + k * 80), a=80)

def painel(d, rnd):
    for i in range(3):
        for j in range(2):
            rect(d, 170 + i * 260, 640 + j * 360, 220, 300, a=120)
            line(d, (190 + i * 260, 680 + j * 360), (370 + i * 260, 680 + j * 360), a=90)

def manchete(d, rnd):
    rect(d, 120, 820, 840, 260, a=150, lw=3)
    line(d, (160, 900), (920, 900), a=110); line(d, (160, 1000), (760, 1000), a=110)

def timeline(d, rnd):
    line(d, (140, 960), (940, 960), a=150, w=3)
    for k in range(7):
        x = 160 + k * 130
        circ(d, x, 960, 16, a=170, lw=3)
        line(d, (x, 960), (x, 880 - (k % 2) * 60), a=90)

def mapa(d, rnd):
    for k in range(40):
        circ(d, rnd.randint(160, 920), rnd.randint(560, 1400), rnd.randint(4, 10), lw=2, a=rnd.randint(80, 170))

def barras(d, rnd):
    for k in range(7):
        h = 120 + rnd.randint(40, 380)
        rect(d, 170 + k * 120, 1340 - h, 80, h, a=130)
    line(d, (140, 1340), (940, 1340), a=130)

def relogio(d, rnd):
    circ(d, 540, 960, 280, lw=3, a=150)
    for k in range(12):
        t = math.radians(k * 30)
        line(d, (540 + 240 * math.cos(t), 960 + 240 * math.sin(t)), (540 + 270 * math.cos(t), 960 + 270 * math.sin(t)), a=130)
    line(d, (540, 960), (540, 760), a=170, w=3); line(d, (540, 960), (660, 1010), a=170, w=3)

def faixa_pop(d, rnd):
    rect(d, 80, 900, 920, 120, a=150, lw=3)
    line(d, (120, 1060), (960, 1060), a=90)

def calendario(d, rnd):
    for c in range(7):
        rect(d, 150 + c * 120, 620, 110, 700, a=110)
        for r in range(5):
            circ(d, 205 + c * 120, 700 + r * 130, 12, a=90)

def contraluz(d, rnd):
    for k in range(8):
        line(d, (540, 960), (540 + 500 * math.cos(math.radians(-90 + k * 45)), 960 + 500 * math.sin(math.radians(-90 + k * 45))), a=70)
    circ(d, 540, 960, 120, a=120)

def interrogacao(d, rnd):
    circ(d, 540, 860, 170, lw=3, a=140)
    line(d, (540, 1060), (540, 1200), a=140, w=3)
    circ(d, 540, 1260, 14, a=170, lw=4)

def cards(d, rnd):
    for k in range(6):
        rect(d, 180 + (k % 2) * 380, 620 + (k // 2) * 300, 320, 240, a=120)

def caixa_misterio(d, rnd):
    rect(d, 200, 760, 680, 400, a=140, lw=3)
    line(d, (200, 900), (880, 900), a=100)
    line(d, (540, 760), (540, 1160), a=100)

def grade_cartas(d, rnd):
    for r in range(3):
        for c in range(4):
            rect(d, 170 + c * 200, 640 + r * 320, 160, 240, a=100)

def pódio(d, rnd):
    rect(d, 220, 1040, 240, 280, a=130)
    rect(d, 420, 900, 240, 420, a=150)
    rect(d, 620, 1100, 240, 220, a=120)

def faixa_chegada(d, rnd):
    for k in range(10):
        rect(d, 160 + k * 80, 800, 80, 80, a=110, lw=1)
    line(d, (140, 1100), (940, 1100), a=130)

def estrela(d, rnd):
    pts = []
    for k in range(10):
        r = 240 if k % 2 == 0 else 100
        t = math.radians(-90 + k * 36)
        pts.append((540 + r * math.cos(t), 960 + r * math.sin(t)))
    d.polygon([(x * S, y * S) for x, y in pts], outline=OURO + (150,), width=3 * S)

def medalhao(d, rnd):
    circ(d, 540, 960, 260, lw=3, a=150)
    circ(d, 540, 960, 220, a=100)
    circ(d, 540, 960, 180, a=70)

def coroa_louros(d, rnd):
    for side in (-1, 1):
        for k in range(8):
            t = math.radians(90 + side * (20 + k * 12))
            x, y = 540 + side * 0 + 260 * math.cos(t) * side, 960 + 260 * math.sin(t)
            circ(d, x, y, 24, a=100)

def placa_dourada(d, rnd):
    rect(d, 160, 720, 760, 480, a=150, lw=3)
    rect(d, 190, 750, 700, 420, a=80, lw=1)

def diagrama(d, rnd):
    for k in range(6):
        y = 620 + k * 180
        line(d, (160, y), (920, y), a=90)
        circ(d, 200 + rnd.randint(0, 680), y, 10, a=150)

# ---------- dias ----------
DIAS = {
 "segunda_prancheta": [campo, setas, circulos, pontos, lousa, tunel, campo],
 "terca_legends": [arquibancada, refletor, cartaz, sala_trofeus, bola, coroa_louros, spot],
 "quarta_tribunal": [dois_lados, balanca, martelo, microfone, votacao, spot, dois_lados],
 "quinta_caixa_preta": [caixa, cofre, lupa, livro, raio_x, ficha, caixa],
 "sexta_giro": [painel, timeline, mapa, barras, relogio, manchete, calendario],
 "sabado_quem_sou_eu": [contraluz, interrogacao, cards, caixa_misterio, spot, grade_cartas, contraluz],
 "domingo_corrida": [pódio, medalhao, faixa_chegada, estrela, placa_dourada, diagrama, coroa_louros],
}

def main():
    os.makedirs(OUT, exist_ok=True)
    for dia, motivos in DIAS.items():
        for i, fn in enumerate(motivos, 1):
            seed = hash((dia, i)) & 0xffff
            rnd = random.Random(seed)
            img = base(seed)
            lay = layer(); d = ImageDraw.Draw(lay)
            fn(d, rnd)
            finish(img, lay, f"{dia}_{i:02d}.jpg")
    print("ok", len(DIAS) * 7, "fundos em", OUT)

if __name__ == "__main__":
    main()
