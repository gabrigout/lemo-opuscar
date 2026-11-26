#!/bin/sh
# Futopia · Campo 3D — demo film, one command. Writes to ${OUT:-/tmp/futopia-campo-out}.
set -e
LIB=${LIB:-/home/user/lemo-opuscar}
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=${OUT:-/tmp/futopia-campo-out}; mkdir -p "$OUT"
cd "$LIB"
node core/render/events.mjs "$HERE" --size 1080x1920 --out "$OUT/events.json"
node core/render/video.mjs "$HERE" --fps 30 --workers ${WORKERS:-3} --size 1080x1920 --out "$OUT/video.mp4"
LIB="$LIB" .venv/bin/python "$HERE/mix.py" "$OUT/events.json" "$OUT/mix.wav"
sh core/render/mux.sh "$OUT/video.mp4" "$OUT/mix.wav" "$OUT/test.mp4" 30 1
node core/render/still.mjs "$HERE" 3.9 --size 1080x1920 --out "$OUT" --prefix poster_
