# FUTGOAT — canal de futebol · dossiê completo para continuar o trabalho

Tagline: **O melhor do futebol** · TikTok + Instagram Reels · 1080×1920, 30 fps
Este dossiê foi escrito em 26/11/2026 para o Claude Code reconstruir o contexto e seguir a produção com a biblioteca Lemo-Opuscar (pasta na raiz do repositório). **Leia este arquivo inteiro antes de agir. O prompt de partida está no final.**

> "Futgoat" é o nome do canal. O dono às vezes escreve "Footnote" ou "Futopia" por engano de ditado: é tudo **Futgoat**. (Futopia foi um nome antigo, descartado.)

---
## 1. Quem é o dono e como trabalhar com ele
- Brasileiro, escreve em **português**. Responda sempre em português do Brasil, direto, sem enrolação. Quando ele pede "só sim ou não", responda só isso.
- Torcedor do Corinthians, mas quer canal **neutro**: sem verde, sem cores de clube, sem escudos, sem favorecer time.
- **Nunca começar a renderização completa de um vídeo sem ele aprovar o roteiro e o plano visual.**
- Tudo o que sai tem de seguir a estética Futgoat (seção 3). "Tudo que você tem em mente seja mudado pra estética que criamos." Linhas **finas e detalhadas**, nunca grossas.
- Não mexer em `core/` nem `styles/` da biblioteca para um filme do usuário. Filmes ficam fora de `styles/`; sem crédito Lemo nem marca d'água.
- Trabalha pelo celular/PC com planos limitados (ferramentas de imagem acabam o limite): peça poucas imagens por vez e dê prompts completos, prontos para colar.
- Quando precisar trocar de modelo para construir/renderizar (Opus 5.5), avise-o: ele ajusta no `/model`.

## 2. Decisões fechadas
| Item | Decisão |
|---|---|
| Nome | **Futgoat** (conferir @ livre; TikTok atual criado: @futegoatt, a decidir) |
| Símbolo | bode GOAT dourado, logo redondo com o nome no anel (`identidade/kit/logo-redondo-futgoat.png`) |
| Assinatura | **O melhor do futebol** (rejeitado: "futebol explicado") |
| Conteúdo | curiosidades e histórias · rankings e debates (GOAT) · notícias · tática e análise. Futebol brasileiro e mundial, neutro |
| Voz | **James** (voz do ElevenLabs que o dono usa), clonada localmente com Chatterbox. Possível voz própria mais grave para o bode: **pendente** |
| Apresentador | **o bode GOAT**: musculoso, jaqueta de treino escura com detalhe dourado, sem escudo. Arte feita pelo dono no Gemini/ChatGPT; o Claude recorta e anima |
| Aparição do bode | pequeno perto da borda esquerda; **cresce com destaque quando fala**. Três níveis: busto, meio corpo (braços/gestos), corpo inteiro (ações) |
| Quadros | Seg **Prancheta** (tática) · Ter **Lendas** (histórias) · Qua **GOAT** (rankings) · Qui **Curiosidade rápida** · Sex **Resumo da semana** · Sáb Desafio e Dom Pré-jogo (opcionais). Começar por Seg/Ter/Qua |
| Plataformas | TikTok e Instagram Reels. Perfil **novo** (não reaproveitar o canal "Por Trás do Mundo") |
| Regras | sem imagem de transmissão, escudos, camisas oficiais ou rosto de jogador real; fatos com fonte; nada de número inventado; sem hashtag com nome do canal; sem vinheta no início, só 1,2 s no fim |

Veja `PLANO.md` para a grade completa de quadros e estilos sugeridos por dia.

## 3. Estética Futgoat (vale para TUDO)
- Paleta: preto quente `#111111` · dourado `#D4A537` · creme `#F2E9D8` · bronze `#8A5A12` · grafite `#2A2A2E` / cinza `#3A3A3C`. **Sem verde, sem branco puro.**
- Fontes: **Anton** (títulos, números) e **Archivo Black** (legendas) em `identidade/fonts/`.
- Linhas finas: marcações do campo 0,07 m, discos R = comprimento/40, setas finas, zonas com anel. Há um estilo próprio já pronto em `estilo-campo/` (cópia do estilo do usuário `~/lemo-my-styles/futgoat-campo/`, "Futgoat Pitch 3D", base Three.js, motor `demo/engine/campo.js`).
- Zona segura: nada abaixo de y≈1440 nem a menos de 180 px da borda direita; título/legenda entre y≈390 e 1530 para sobreviver ao corte 3:4 do grid do Instagram. Hook nos primeiros 1,5–3 s. Duração 30–60 s.
- Entrega por vídeo: mp4, `.srt`, capa **separada** (template em `identidade/capa/`, parâmetros `?tag=&l1=&l2=`), legenda de postagem com SEO para TikTok e para Instagram (texto copiável, sem hashtag com nome do canal).

## 4. O que já existe nesta pasta
| Caminho | Conteúdo |
|---|---|
| `PLANO.md` | plano geral e decisões |
| `identidade/` | logo, foto de perfil, vinheta de 1,2 s (`kit/`, `vinheta/`), modelo de capa (`capa/`), fontes, `PADRAO-REDES.md` (padrões de TikTok/Instagram pesquisados) |
| `apresentador/` | bode: base busto/meio/inteiro (PNG e recortes sem fundo), estados de boca/olhos (`estados/`), demo de sincronia labial (`exemplo-lipsync/index.html` + `sync.json`) |
| `estilo-campo/` | estilo "Futgoat Pitch 3D" (STYLE.md, demo e motor 3D) |
| `pilotos/prancheta-01/ROTEIRO.md` | piloto "Prancheta Nº 1: o 2-3-1 do society" (8 falas, ~50 s), **aguardando aprovação do dono** |
| `voz-banco/` | `vocabulario.json` (33 frases-base), `gerar_banco.py`, `montar.py` (banco de voz próprio) |

**Não estão no repositório de propósito** (repositório público): áudios e referência de voz do James, vídeos de teste e arquivos pesados. Recrie-os (seção 6).

## 5. Fluxo de produção de um vídeo
1. Tema → 2. pesquisa/fontes → 3. roteiro com gancho + entradas do bode marcadas → 4. escolha de 1–2 estilos → 5. **aprovação do dono** → 6. voz (gerar, conferir com Whisper) → 7. animação (HTML + `window.render(t)`) → 8. trilha e mix (−14 LUFS, `mux.sh`) → 9. render → 10. revisão (fatos, leitura, som) → entrega (mp4, srt, capa, legenda SEO).
Siga `AGENTS.md`, `DIRECTOR.md`, `TECHNIQUE.md` da biblioteca: escrever `TREATMENT.md` **antes** de abrir demos de estilo.

## 6. Reconstruir o ambiente (lições aprendidas)
- **ffmpeg ≥ 7** é obrigatório (rubberband/loudnorm). Em ambiente sem permissão de instalar: `imageio-ffmpeg` + symlink no projeto e `PATH` com ele na frente.
- **Voz local (Chatterbox multilingual, CPU, ~1 min por fala):** venv com `chatterbox-tts faster-whisper num2words imageio-ffmpeg "setuptools<81"` (sem o setuptools antigo a marca d'água `perth` falha).
  Geração: `ChatterboxMultilingualTTS.from_pretrained(device="cpu")`; `model.generate(texto, language_id="pt", audio_prompt_path=ref, exaggeration=0.5, cfg_weight=0.3)`.
- **Referência da voz:** `ref_james_12s.wav` = 12 s limpos cortados de um mp3 do James (ElevenLabs) que o dono tem. Peça os mp3 se não estiverem na máquina; coloque o wav em `voz-banco/`.
- Se o ambiente for em nuvem com rede restrita, liberar hosts do HuggingFace (`huggingface.co`, `cas-server.xethub.hf.co`, `us.aws.cdn.hf.co`) para baixar os modelos.
- **Conferir a voz:** transcrever com Whisper "small" e comparar com o texto **normalizando números por extenso** (`num2words`). Aceitar razão ≥ 0.93. Whisper erra palavra em inglês (ex.: "society" → "seu site"): não é falha da voz, confira à mão.
- **Sincronia:** timestamps por palavra do Whisper; boca por RMS do áudio; legendas e eventos saem desses tempos. Nunca fixe tempos antes da voz final.
- **Recorte do bode (fundo magenta #FF00FF):** limiar por distância, remover reflexo magenta (despill), trocar cor das bordas pela do interior; **nunca** preencher buracos em fundo magenta (apaga olhos/chifres que são escuros). Trocas de rosto entre variações do Gemini funcionam porque as imagens alinham em (0,0).
- **Render 3D** (`campo.js`) em WebGL por software: ~0,3–0,5 s/quadro. Texturas de número em 512 px, fonte Anton 330 px.
- Git: o dono tem repositório público `gabrigout/lemo-opuscar`; **autorizou** guardar o Futgoat aqui. Nunca subir áudios de voz nem dados pessoais.

## 7. Banco de voz ("dossiê de palavras")
Objetivo: não depender de créditos do ElevenLabs; ter a voz do James "para sempre".
- Frase-base em `voz-banco/vocabulario.json` (cobre dias, quadros, posições, esquemas, números 1–100, conectores, competições, reações, chamadas para seguir/comentar). Todas as 8 falas do piloto estão incluídas.
- `gerar_banco.py`: gera cada frase localmente, confere com Whisper, indexa **cada palavra com início/fim** em `index.json`; retoma de onde parou.
- `montar.py "texto novo" saida.wav`: monta frase nova reaproveitando os **trechos mais longos** do banco (fades de 15 ms, pausas por pontuação) e gera localmente só o que falta. Palavra solta colada soa robótica: prefira trechos grandes e gerar o resto.
- **Plano com os 10 mil créditos do ElevenLabs:** o dono quer gastar créditos uma vez para ter o banco na melhor qualidade. Ele gera no ElevenLabs (voz James) as frases de `vocabulario.json` + as que o Claude listar, envia os mp3, e o Claude os indexa com Whisper do mesmo jeito (`index.json`) para o `montar.py` usar. Assim o banco fica com a qualidade do ElevenLabs e o resto vem do Chatterbox.
- Guardar o banco (audios + index.json) **fora** do repositório público, em zip entregue ao dono.

## 8. Estado e pendências (26/11/2026)
Feito: identidade (logo/perfil/vinheta/capa), estilo de campo 3D dourado/preto com linhas finas, bode em 3 níveis (busto com estados de boca; meio e inteiro em base), demo de sincronia labial, roteiro do piloto, banco de voz em geração.
Pendente com o dono:
1. aprovar o roteiro do piloto (`pilotos/prancheta-01/ROTEIRO.md`);
2. voz do bode: James ou uma mais grave própria;
3. imagens do Gemini para poses essenciais: meio-apontando, meio-explicando, inteiro-chutando, inteiro-comemorando;
4. moldura: medalhão redondo com a cabeça saindo vs. barra dourada;
5. @ do TikTok (@futegoatt vs @futgoat.fut / @ofutgoat), bio (TikTok ≤80 chars, Instagram ≤150), criar Instagram;
6. banco de voz com os créditos do ElevenLabs (seção 7).
Depois: construir o piloto (campo 3D animado, bode falando nas falas 3 e 7 com sincronia labial, trilha e foley, legendas na zona segura, vinheta final 1,2 s, capa, legenda SEO), então formato dos outros quadros, banco de pautas, rotina e horários.

---
## 9. PROMPT PARA COLAR NO CLAUDE CODE

```
Estou continuando o canal de futebol FUTGOAT (tagline "O melhor do futebol"; TikTok e Instagram Reels, 1080x1920, 30 fps) com a biblioteca Lemo-Opuscar desta pasta. Eu escrevo em português do Brasil; responda sempre em português, direto.

1) Leia primeiro, na ordem: futgoat/README.md (tudo: decisões, estética, regras, lições técnicas, pendências), futgoat/PLANO.md, futgoat/identidade/PADRAO-REDES.md, futgoat/pilotos/prancheta-01/ROTEIRO.md, futgoat/estilo-campo/STYLE.md. Depois AGENTS.md, DIRECTOR.md e TECHNIQUE.md da biblioteca. Não abra DEMO.md de estilos antes de escrever o TREATMENT.md.

2) Recrie o ambiente: ffmpeg >= 7, node, e um venv Python com chatterbox-tts, faster-whisper, num2words, imageio-ffmpeg e "setuptools<81". Copie futgoat/estilo-campo para ~/lemo-my-styles/futgoat-campo/ (e registre a linha em ~/lemo-my-styles/README.md) para o estilo "Futgoat Pitch 3D" funcionar. Crie a pasta de trabalho films/futgoat/ (ignorada pelo git) copiando de futgoat/ o que precisar. Não suba áudios de voz para o git.

3) Voz: vou te dar os mp3 do James (ElevenLabs). Corte uma referência limpa de 12 s (ref_james_12s.wav) em futgoat/voz-banco/, rode futgoat/voz-banco/gerar_banco.py (Chatterbox local, conferido pelo Whisper com números por extenso) para criar o banco de voz indexado por palavra, e valide montar.py gerando uma frase nova que eu possa ouvir. Depois integre os áudios do ElevenLabs que eu enviar ao mesmo index.json.

4) Aplique a estética Futgoat em TUDO: preto #111111, dourado #D4A537, creme #F2E9D8, bronze #8A5A12, grafite #2A2A2E/#3A3A3C; sem verde e sem branco puro; fontes Anton e Archivo Black; linhas finas e detalhadas; zona segura (nada abaixo de y~1440 nem a menos de 180 px da borda direita; conteúdo central entre y~390 e 1530).

5) Piloto: me mostre o roteiro da Prancheta Nº 1 (o 2-3-1 do society) e espere minha aprovação ANTES de gastar tempo de render. Só depois: gere a voz do piloto (8 falas, conferidas), animação no estilo Futgoat Pitch 3D, o bode (apresentador) pequeno na borda esquerda e crescendo ao falar nas falas 3 e 7 com sincronia labial pelos estados em futgoat/apresentador/estados, trilha e foley, legendas, vinheta final de 1,2 s, mix -14 LUFS, capa separada, .srt e legendas de postagem (TikTok e Instagram, com SEO, sem hashtag com o nome do canal).

6) Regras fixas: nunca renderizar o vídeo completo sem eu aprovar roteiro e plano visual; canal neutro (sem clubes, escudos, jogadores reais ou imagens de transmissão); sem número inventado; peça-me imagens do Gemini só quando for indispensável, com prompts completos prontos para colar.

7) Comece listando o que falta de mim (imagens de pose, decisões de voz/moldura/@) e o que você já pode fazer sozinho, e faça o que puder sem me perguntar nada.
```

---
## 10. Vocabulário para gerar no ElevenLabs (créditos do dono)
Arquivo: `voz-banco/PARA-ELEVENLABS.txt` (5 blocos A–E, ~8 mil caracteres; 1 caractere = 1 crédito, a conferir no plano) e `voz-banco/vocabulario_elevenlabs.json`.
Processo: o dono gera cada bloco no ElevenLabs com a voz James e as mesmas configurações, baixa um mp3 por bloco e manda ao Claude. O Claude transcreve com Whisper, corta por frase/palavra e monta o `index.json` do banco (mesma estrutura do `gerar_banco.py`). Gere o **bloco A primeiro**: confira a pronúncia de "Futgoat" e dos nomes antes de gastar o resto.
