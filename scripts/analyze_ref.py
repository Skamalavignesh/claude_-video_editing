#!/usr/bin/env python3
"""Measure a reference reel's style: duration, cuts, avg shot length, loudness. Usage: analyze_ref.py <video> [--json out.json]"""
import argparse, json, subprocess, re
from scenedetect import detect, ContentDetector

ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("--json")
a = ap.parse_args()
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                     "-of", "default=nw=1:nk=1", a.video]).decode())
scenes = detect(a.video, ContentDetector(threshold=27))
cuts = [round(s[0].get_seconds(), 2) for s in scenes[1:]]
lufs = None
r = subprocess.run(["ffmpeg", "-i", a.video, "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
m = re.search(r'"input_i"\s*:\s*"(-?[\d.]+)"', r)
if m: lufs = float(m.group(1))
res = {"file": a.video, "duration_s": round(dur, 2), "num_shots": len(scenes),
       "avg_shot_len_s": round(dur / max(len(scenes), 1), 2), "cuts_per_min": round(len(cuts) / dur * 60, 1),
       "cut_times": cuts, "loudness_lufs": lufs}
print(json.dumps(res, indent=1))
if a.json: json.dump(res, open(a.json, "w"), indent=1)
