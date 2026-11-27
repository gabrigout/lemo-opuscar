# Voz do Goat (decidida em 27/11/2026)

- Motor: Kokoro (kokoro-onnx), offline, Apache 2.0. Modelo: kokoro-v1.0.onnx e voices-v1.0.bin (Hugging Face: fastrtc/kokoro-onnx), em core/tts/.
- Voz: pm_santa (masculina, pt-BR), lang "pt-br", speed 1.05.
- Pós-processamento: pitch +3 semitons (ffmpeg rubberband=pitch=1.1892), saída 44,1 kHz.
- Pronúncia: no texto enviado à voz, escrever "Gôut" no lugar de "Goat" e "Futgôut" no lugar de "Futgoat". Legendas usam o texto original.
- Frases geradas uma a uma, com 0,35 s de pausa entre elas.
- Encerramento continua com voz feminina (sem o Goat na tela).
- Ferramentas: core/tts/tts.py gera as frases; a sincronia de boca e legenda usa o Whisper com o texto do roteiro como referência.
