# Convite XV Anos — Maria Fernanda

Site estático (HTML, CSS e JS puros). Não precisa instalar nada para publicar.

```
index.html              página (estrutura)
assets/css/style.css    visual
assets/js/app.js        ← AQUI ficam data, local, telefone e textos (objeto CONFIG, no topo)
assets/musica.mp3       música de fundo (placeholder: troque pelo arquivo que você escolher)
assets/img/preview.jpg  imagem que aparece quando o link é colado no WhatsApp
assets/img/favicon.svg  ícone da aba do navegador
```

## O que você precisa trocar (antes de publicar)

| # | O quê | Onde | Obrigatório? |
|---|-------|------|--------------|
| 1 | **Número do WhatsApp** (DDD + número) | `assets/js/app.js` → `whatsapp: ""` (ex.: `"91988887777"`) | **Sim.** Vazio, o WhatsApp abre pedindo para escolher um contato. |
| 2 | **Música** | Substitua `assets/musica.mp3` (mesmo nome, formato MP3, ideal até ~3 MB) | Recomendado. A que está lá é uma valsa instrumental curta, gerada só como placeholder. |
| 3 | **Lista ou link de presentes** | `assets/js/app.js` → `presentes.itens` (lista) e/ou `presentes.linkUrl` (link) | **Sim.** Sem isso, a janela mostra o texto `[PLACEHOLDER]`. |
| 4 | Link da imagem de pré-visualização | `index.html` → `og:image`: troque pelo endereço completo (veja "Depois de publicar") | Opcional, mas deixa o link bonito no WhatsApp. |
| 5 | Duração da festa (só afeta a agenda) | `assets/js/app.js` → `evento.duracaoHoras` (hoje: 5 horas) | Confira. É uma suposição. |

Tudo o mais (nome, data, hora, local, traje, textos, itens do Manual do Convidado, mensagens do WhatsApp) também está no `CONFIG`, no topo de `assets/js/app.js`. Edite com o Bloco de Notas ou qualquer editor de texto. Mantenha as aspas e as vírgulas.

Se mudar o nome ou a data, ajuste também o `<title>` e as tags `og:` no começo do `index.html`, e refaça `assets/img/preview.jpg` se quiser.

## Testar no computador

Dentro da pasta, rode:

```
python3 -m http.server 8000
```

e abra http://localhost:8000. Para ver no celular, conecte-o na mesma rede Wi-Fi e abra `http://IP-DO-COMPUTADOR:8000`.
(Abrir o `index.html` com duplo clique também costuma funcionar, mas o teste pelo servidor é mais fiel ao que o convidado vai ver.)

## Publicar de graça e gerar o link para o WhatsApp

### Opção A — Netlify Drop (mais fácil, ~2 minutos)
1. Faça as trocas acima.
2. Abra https://app.netlify.com/drop
3. Arraste a **pasta inteira** (a que contém o `index.html`) para a área indicada.
4. Em segundos aparece um link como `https://nome-aleatorio.netlify.app`.
5. Crie uma conta gratuita (ou entre) quando o Netlify pedir: sem conta, o site de teste pode expirar em pouco tempo.
6. Para um endereço mais bonito: *Site configuration → Change site name* (ex.: `maria-xv`).
7. Para atualizar depois: aba *Deploys* → arraste a pasta de novo.

### Opção B — GitHub Pages
1. Crie uma conta em https://github.com e depois um repositório novo (público), por exemplo `xv-maria`.
2. Em *Add file → Upload files*, arraste o `index.html` e a pasta `assets` e clique em *Commit changes*.
3. *Settings → Pages → Build and deployment*: *Source: Deploy from a branch*, *Branch: main*, pasta *`/ (root)`* → *Save*.
4. Em 1–2 minutos o link aparece no topo da página: `https://SEU-USUARIO.github.io/xv-maria/`.

### Depois de publicar
1. Abra o link no celular, toque no lacre e teste cada botão (principalmente "Confirmar presença", para ver se chega no número certo).
2. (Opcional) Pré-visualização bonita no WhatsApp: no `index.html`, troque `content="assets/img/preview.jpg"` pelo endereço completo, por exemplo `content="https://maria-xv.netlify.app/assets/img/preview.jpg"`, e publique de novo. O WhatsApp guarda a pré-visualização em cache; se já mandou o link antes, mande um com `?v=2` no final.
3. Cole o link no WhatsApp e envie.

## Observações técnicas

- A música só começa depois do toque no lacre (regra dos navegadores). O botão no canto superior direito silencia/ativa; a música pausa quando a pessoa sai da página (por exemplo, para o WhatsApp) e volta ao retornar.
- Em iPhone, o volume da música é o do aparelho (o Safari ignora o controle de volume da página).
- Para quem ativa "reduzir movimento" no celular, o envelope abre sem a animação longa.
- O arquivo de agenda (.ics) usa horário universal, então aparece certo em qualquer fuso, e já inclui lembrete 1 dia antes.
- O site depende apenas do Google Fonts (Cormorant Garamond e Great Vibes). Sem internet, usa fontes parecidas do aparelho.
