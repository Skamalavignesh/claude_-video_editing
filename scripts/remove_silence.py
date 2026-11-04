#!/usr/bin/env python3
"""Suggest keep-ranges by removing silence, as EDL JSON. Usage: remove_silence.py <media> <out.json> [--db -35] [--min 0.35] [--pad 0.08]"""
import argparse, json, re, subprocess
ap = argparse.ArgumentParser()
ap.add_argument("media"); ap.add_argument("out")
ap.add_argument("--db", type=float, default=-35); ap.add_argument("--min", type=float, default=0.35)
ap.add_argument("--pad", type=float, default=0.08)
a = ap.parse_args()
dur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",a.media]))
log = subprocess.run(["ffmpeg","-i",a.media,"-af",f"silencedetect=noise={a.db}dB:d={a.min}","-f","null","-"],
                     capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
keep, cur = [], 0.0
for s, e in zip(starts, ends):
    if s - cur > 0.1: keep.append([max(cur - a.pad, 0), min(s + a.pad, dur)])
    cur = e
if dur - cur > 0.1: keep.append([max(cur - a.pad, 0), dur])
json.dump({"clips": [{"src": a.media, "in": round(i,3), "out": round(o,3)} for i, o in keep]}, open(a.out, "w"), indent=1)
print(f"{len(keep)} segments, kept {sum(o-i for i,o in keep):.1f}s of {dur:.1f}s")
