# Voz do Goat (decidida em 27/11/2026, substitui as anteriores)

**Regra de trabalho:** o dono lê o roteiro com a própria voz no celular e manda o áudio. O Claude limpa, corta, troca o timbre pelo da **Skylo** (ElevenLabs, voz "Crazy & Funny") e monta o vídeo. A interpretação (ritmo, emoção, pausas) é sempre a do dono.

## Passo a passo (pasta pipeline/)
1. Converter o áudio do celular para wav (ffmpeg) e transcrever com Whisper com tempo por palavra (`tr.py`).
2. Achar a claquete, as tomadas repetidas e os escorregões de fato. Ficar com a última tomada boa de cada frase.
3. Limpeza leve da gravação inteira (corte de grave 70 Hz, redução de chiado bem leve, um pouco de presença, compressão 2:1), antes de cortar.
4. Cortar nos vales de energia entre falas, nunca em tempo de palavra do Whisper (o tempo do Whisper erra por até ~0,3 s e deixa sobra da frase vizinha). Conferir cada emenda (`corta.py`).
5. Conversão de voz: Chatterbox VC (`chatterbox.vc.ChatterboxVC`), trecho por trecho, alvo = 13 s limpos da Skylo (`alvo_skylo.wav`, cortado do mp3 do ElevenLabs, entre 1:15 e 1:28, fala "Futgoat"). Versão pura (100%) por padrão; misturar 30 a 50% com a voz original se a fala embolar (`convert_all.py`).
6. Montar trilha, efeitos e sincronia de boca/legendas (`build2.py`) e renderizar com a biblioteca (`core/render/video.mjs`, `--size 1080x1920`).
7. Mux final em -14 LUFS com `core/render/mux.sh`; o encerramento é a voz feminina (Lauren), sem o Goat.

## Limites conhecidos
- O conversor é treinado sobretudo em inglês: em português ele embola um pouco as consoantes, em especial nomes próprios. Legendas usam a grafia certa do roteiro.
- Erros de fato que o dono falar (nome de time, jogador, número) são cortados e sinalizados; ele pode regravar só a frase.
- Áudios e referências de voz NÃO vão para o GitHub (repositório público).
- O disco da sessão é limitado: não baixar modelos grandes sem necessidade.
