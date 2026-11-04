#!/usr/bin/env bash
# Low-res proxies (fast to analyze/upload). Usage: make_proxy.sh <project>
set -euo pipefail
P="projects/$1"
for f in "$P"/raw/*; do
  [ -f "$f" ] || continue
  b=$(basename "${f%.*}")
  ffmpeg -y -loglevel error -i "$f" -vf "scale=-2:540,fps=30" -c:v libx264 -preset veryfast -crf 28 -c:a aac -b:a 96k "$P/proxies/$b.mp4"
  echo "proxy: $P/proxies/$b.mp4"
done
