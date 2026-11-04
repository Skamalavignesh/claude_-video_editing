# Reels AI-Editing Workflow

Give Claude references + a brief; get a pro-level vertical reel with approval gates. Claude drives ffmpeg-based tools through an EDL.

## Quick start
```bash
./setup.sh                               # installs ffmpeg, venv, whisper, scenedetect; runs doctor
./scripts/new_project.sh my-first-reel   # scaffold project + brief
# edit brand/brand-kit.md, add refs/ + refs/notes.md, drop footage in projects/my-first-reel/raw/, fill brief.md
claude                                   # open Claude Code here, then paste prompts/kickoff-prompt.md
```
Windows: use WSL (recommended) or Git Bash.

## How it works
`CLAUDE-BOOTSTRAP.md` is a single portable file to hand to any other Claude Code session (it clones + sets up). `CLAUDE.md` is the editor's playbook (7 steps, 3 approval gates, reels craft rules). Claude cannot watch video, so it uses transcripts,
contact sheets, scene/loudness measurements and an EDL (`edl.json`), then `scripts/render_edl.py` renders it.

| Script | Purpose |
|---|---|
| `doctor.sh` | verify toolchain |
| `make_proxy.sh` | 540p proxies for fast analysis |
| `contact_sheet.sh` | frame grid so Claude can see a clip |
| `transcribe.py` | word-level transcript (JSON + SRT) |
| `analyze_ref.py` | reference style: cuts/min, avg shot length, LUFS |
| `remove_silence.py` | silence-trimmed EDL |
| `render_edl.py` | EDL -> 1080x1920 reel (music ducking, captions, loudnorm); `--preview` for 540p |
| `qa_check.sh` | technical QA |

## Folder map
`refs/` references · `brand/` brand kit · `prompts/` brief + kickoff + EDL example · `checklists/` setup + QA · `projects/<name>/` per-reel work.

## Limits
Claude judges visuals via frames/transcripts, so use the gates and give timestamped notes. Footage isn't stored in git.
Motion graphics beyond burned captions: use the invideo or Canva connector from Claude.
