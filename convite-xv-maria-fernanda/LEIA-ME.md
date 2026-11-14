# Convite XV Anos — Maria Fernanda

Site estático (HTML, CSS e JS puros). Não precisa instalar nada para publicar.

```
index.html              página (estrutura)
assets/css/style.css    visual
assets/js/app.js        ← AQUI ficam data, local, telefone e textos (objeto CONFIG, no topo)
assets/musica.mp3       música de fundo (instrumental; pode trocar pelo arquivo que preferir)
assets/img/preview.jpg  imagem que aparece quando o link é colado no WhatsApp
assets/img/favicon.svg  ícone da aba do navegador
```

## O que já está preenchido

| Item | Valor |
|------|-------|
| WhatsApp que recebe as respostas | (91) 98520-4553 |
| Data e hora | quinta-feira, 17 de dezembro de 2026, 21h |
| Local | Le Lys Maison, Travessa São Francisco, 60, Campina, Belém/PA |
| Traje | esporte fino |
| Presentes | lista em grupos (roupas, calçados, acessórios, perfumes, maquiagem, lojas) |
| Prazo para confirmar | até 10 de dezembro |
| Convite | individual (não pergunta quantidade de pessoas) |
| Horário de término | não informado: no calendário do convidado o evento aparece com 5 horas de duração (`evento.duracaoHoras`) |

## O que ainda dá para ajustar

| O quê | Onde |
|-------|------|
| **Música** | Substitua `assets/musica.mp3` (mesmo nome, formato MP3, ideal até ~3 MB). A que está lá é uma valsa instrumental curta, feita só como placeholder. Se usar música de artista, lembre que ela vai ficar pública no site. |
| Link da imagem de pré-visualização no WhatsApp | `index.html` → `og:image` (troque pelo endereço completo depois de publicar; veja abaixo) |
| Permitir acompanhantes | `assets/js/app.js` → `rsvp.maxPessoas` (hoje `1`; com `2` ou mais, volta o seletor "quantidade de pessoas") |
| Prazo, presentes, textos, itens do Manual, mensagens do WhatsApp | `CONFIG`, no topo de `assets/js/app.js` |

Edite com o Bloco de Notas ou qualquer editor de texto. Mantenha as aspas e as vírgulas.
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
1. Entre em https://app.netlify.com/drop e **crie a conta gratuita primeiro** (pode ser com o Google). Sem estar logado, o link fica protegido por senha temporária e expira.
2. Já logado, volte para https://app.netlify.com/drop
3. Arraste a **pasta inteira** (a que contém o `index.html` e a pasta `assets`) para a área indicada.
4. Em segundos aparece um link como `https://nome-aleatorio.netlify.app`.
5. Para um endereço mais bonito: *Site configuration → Change site name* (ex.: `maria-xv`).
6. Para atualizar depois: aba *Deploys* → arraste a pasta de novo. O link continua o mesmo.

No plano gratuito do Netlify, cada publicação custa 15 dos 300 créditos mensais, e o tráfego de ~100 convidados consome muito pouco (cada visita baixa cerca de 0,9 MB). Dá para fazer dezenas de ajustes sem problema. As tarifas mudam de tempos em tempos: confira em https://www.netlify.com/pricing/

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

- Todas as confirmações, músicas e recados chegam no mesmo WhatsApp. Cada mensagem já vem com o nome da pessoa. Com ~100 convidados, considere usar um número só para o convite ou o WhatsApp Business, que permite etiquetar as conversas.
- A música só começa depois do toque no lacre (regra dos navegadores). O botão no canto superior direito silencia/ativa; a música pausa quando a pessoa sai da página (por exemplo, para o WhatsApp) e volta ao retornar.
- Em iPhone, o volume da música é o do aparelho (o Safari ignora o controle de volume da página).
- Para quem ativa "reduzir movimento" no celular, o envelope abre sem a animação longa.
- O arquivo de agenda (.ics) usa horário universal, então aparece certo em qualquer fuso, e já inclui lembrete 1 dia antes.
- O site depende apenas do Google Fonts (Cormorant Garamond e Great Vibes). Sem internet, usa fontes parecidas do aparelho.
