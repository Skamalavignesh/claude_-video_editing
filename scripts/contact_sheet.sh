#!/usr/bin/env bash
# Frame grid so Claude can SEE a clip. Usage: contact_sheet.sh <video> <out.jpg> [every_n_seconds=2]
set -euo pipefail
N="${3:-2}"
ffmpeg -y -loglevel error -i "$1" -vf "fps=1/$N,scale=270:-2,tile=6x6" -frames:v 1 -q:v 3 "$2"
echo "$2"
