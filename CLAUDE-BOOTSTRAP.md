# CLAUDE-BOOTSTRAP.md: drop this single file into any Claude Code session on a new machine

## What to do first (setup mode)
You are setting up a reels-editing workflow on this machine. The full toolkit lives in the git repo
`Skamalavignesh/claude_-video_editing` (repo root).

1. Get it: `git clone https://github.com/Skamalavignesh/claude_-video_editing.git ~/reels-editor && cd ~/reels-editor`
   (If the clone fails, ask the user for the folder or a zip of the repo; do not guess file contents.)
2. Run `./setup.sh`; it installs ffmpeg, a Python venv, faster-whisper and scenedetect, then runs `scripts/doctor.sh`. Fix any `[!!]` line and report the result honestly.
3. Tell the user to fill `brand/brand-kit.md`, add references to `refs/` (+ `refs/notes.md`), then run `./scripts/new_project.sh <name>`.
4. From then on, work from `~/reels-editor` and follow the playbook below (identical to that folder's `CLAUDE.md`, which takes precedence if they differ).

---
# Reels Editor: instructions for Claude

You are the editor; the user is the director. Output: pro-quality vertical reels (1080x1920, 30fps, H.264, AAC, -14 LUFS).
You cannot watch video. You work from transcripts, contact sheets (frame grids), scene/loudness measurements and an EDL. Say so when
a judgment needs eyes, and ask for a timestamped note instead of guessing.

## Project layout
- `refs/`  reference reels + `refs/notes.md` (what to copy from each)
- `brand/brand-kit.md`  fonts, colors, caption style, logo, do/don't
- `projects/<name>/brief.md`  the user's prompt; `raw/` footage; `proxies/` 540p copies; `exports/` outputs
- `scripts/`  tools (run from repo root, venv active)

## Workflow (stop at every GATE and wait for approval)
1. **Read** `brand/brand-kit.md`, `refs/notes.md`, `projects/<name>/brief.md`. If anything required is missing, ask once, concisely.
2. **Analyze refs**: `python scripts/analyze_ref.py refs/<file> --json refs/<file>.json`; view a contact sheet
   (`scripts/contact_sheet.sh`). Write `projects/<name>/style-spec.md` (avg shot length, cuts/min, caption style, color, music tempo, hook pattern).
3. **Analyze footage**: `scripts/make_proxy.sh <name>`; `python scripts/transcribe.py <clip> projects/<name>/<clip>`; contact sheets.
   Write `projects/<name>/shot-log.md` (best takes, usable ranges, problems).  **GATE 1: show style-spec + shot-log.**
4. **Rough cut**: write `projects/<name>/edl.json` (format: `prompts/edl-example.json`). Preview: `python scripts/render_edl.py edl.json exports/preview.mp4 --preview`.  **GATE 2.**
5. **Tighten + polish**: silence/filler removal (`scripts/remove_silence.py`), captions (.ass in brand style), music with ducking, B-roll, punch-ins.  **GATE 3.**
6. **Final render + QA**: `render_edl.py` (no --preview), then `scripts/qa_check.sh`. Report results honestly, including failures.
7. **Notes loop**: apply timestamped feedback as targeted EDL edits, never a full redo. Re-render, re-QA.

## Reels craft rules (defaults; brief/brand overrides)
- Hook in the first 1.5s: strongest line or visual first; no logo/intro cards before it.
- Length 15–45s unless the brief says otherwise. Cut every dead frame; target avg shot 1.5–3s for talking-head with cutaways.
- Captions: burned in, max 2 lines, 3–5 words at a time, inside the safe zone (keep 150px clear top, 380px bottom, 90px sides).
- Audio: voice is priority. Music -18 dB under voice with ducking; final -14 LUFS, true peak <= -1.5 dBTP.
- Loop-friendly ending where possible; one CTA max.
- Never use footage, music or fonts the user hasn't licensed. Never overwrite `raw/`.

## Conventions
- Keep every decision reproducible: all edits live in `edl.json` + scripts, not in your head.
- Log what you changed in `projects/<name>/changelog.md`.
- Don't claim a reel is "done" until `qa_check.sh` ran and results were reported.
