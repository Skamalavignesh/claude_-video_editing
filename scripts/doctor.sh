#!/usr/bin/env bash
# Verify the toolchain.
cd "$(dirname "$0")/.."
ok(){ printf '  [ok]  %s\n' "$1"; }; bad(){ printf '  [!!]  %s\n' "$1"; FAIL=1; }
FAIL=0
command -v ffmpeg >/dev/null && ok "ffmpeg $(ffmpeg -version | head -1 | cut -d' ' -f3)" || bad "ffmpeg missing"
command -v ffprobe >/dev/null && ok ffprobe || bad "ffprobe missing"
ffmpeg -hide_banner -filters 2>/dev/null | grep -q " ass " && ok "libass (burned captions)" || bad "ffmpeg lacks libass; captions burn-in will fail"
ffmpeg -hide_banner -filters 2>/dev/null | grep -q loudnorm && ok loudnorm || bad "loudnorm missing"
PY=python3; [ -x .venv/bin/python ] && PY=.venv/bin/python; [ -x .venv/Scripts/python ] && PY=.venv/Scripts/python
$PY -c "import faster_whisper" 2>/dev/null && ok faster-whisper || bad "faster-whisper not installed (run setup.sh)"
$PY -c "import scenedetect" 2>/dev/null && ok pyscenedetect || bad "scenedetect not installed (run setup.sh)"
command -v claude >/dev/null && ok "claude code" || echo "  [--]  claude code not found (optional but needed to drive the workflow)"
exit $FAIL
