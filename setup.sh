#!/usr/bin/env bash
# One-shot setup for the Reels AI-editing workflow. Supports macOS, Debian/Ubuntu, Windows (WSL/Git-Bash).
set -euo pipefail
cd "$(dirname "$0")"

say(){ printf '\n\033[1;36m==> %s\033[0m\n' "$*"; }
need(){ command -v "$1" >/dev/null 2>&1; }

say "1/5 Installing ffmpeg"
if need ffmpeg && need ffprobe; then echo "ffmpeg already installed"
elif [[ "$OSTYPE" == darwin* ]]; then brew install ffmpeg
elif need apt-get; then sudo apt-get update && sudo apt-get install -y ffmpeg python3-venv fonts-dejavu
elif need winget; then winget install -e --id Gyan.FFmpeg
else echo "Install ffmpeg manually: https://ffmpeg.org/download.html"; exit 1; fi

say "2/5 Python virtualenv"
need python3 || { echo "Install Python 3.10+"; exit 1; }
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate
pip install --upgrade pip
pip install -r requirements.txt

say "3/5 Project folders"
mkdir -p refs brand projects exports

say "4/5 Claude Code"
if need claude; then echo "Claude Code found: $(claude --version 2>/dev/null || true)"
else echo "Install Claude Code: npm install -g @anthropic-ai/claude-code   (or see https://docs.claude.com/claude-code)"; fi

say "5/5 Verifying"
bash scripts/doctor.sh
echo; echo "Done. Next: edit brand/brand-kit.md, drop refs in refs/, then: ./scripts/new_project.sh my-first-reel"
