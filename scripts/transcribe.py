#!/usr/bin/env python3
"""Word-level transcript -> JSON + SRT. Usage: transcribe.py <media> <out_prefix> [--model small]"""
import argparse, json
from faster_whisper import WhisperModel

ap = argparse.ArgumentParser()
ap.add_argument("media"); ap.add_argument("out"); ap.add_argument("--model", default="small")
a = ap.parse_args()
model = WhisperModel(a.model, compute_type="int8")
segs, info = model.transcribe(a.media, word_timestamps=True, vad_filter=True)

def ts(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02}:{int(m):02}:{int(s):02},{int((s % 1) * 1000):03}"

out, srt = [], []
for i, s in enumerate(segs, 1):
    out.append({"start": s.start, "end": s.end, "text": s.text.strip(),
                "words": [{"w": w.word.strip(), "start": w.start, "end": w.end} for w in s.words]})
    srt.append(f"{i}\n{ts(s.start)} --> {ts(s.end)}\n{s.text.strip()}\n")
json.dump({"language": info.language, "segments": out}, open(a.out + ".json", "w"), indent=1)
open(a.out + ".srt", "w").write("\n".join(srt))
print(f"wrote {a.out}.json / .srt  ({info.language})")
