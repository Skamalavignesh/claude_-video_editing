#!/usr/bin/env python3
"""Render an EDL (JSON) into a vertical 1080x1920 reel with optional music, captions, loudness norm.
EDL format (see prompts/edl-example.json):
 {"clips":[{"src":"a.mp4","in":1.2,"out":4.8}, ...], "music":"track.mp3", "music_db":-18,
  "captions_ass":"caps.ass", "fps":30}
Usage: render_edl.py <edl.json> <out.mp4> [--preview]   (--preview = 540p fast render)"""
import argparse, json, subprocess, tempfile, os
ap = argparse.ArgumentParser(); ap.add_argument("edl"); ap.add_argument("out"); ap.add_argument("--preview", action="store_true")
a = ap.parse_args()
e = json.load(open(a.edl)); W, H = (540, 960) if a.preview else (1080, 1920); fps = e.get("fps", 30)
base = os.path.dirname(os.path.abspath(a.edl))
rp = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
inputs, fc, labels = [], [], ""
for i, c in enumerate(e["clips"]):
    inputs += ["-i", rp(c["src"])]
    fc.append(f"[{i}:v]trim={c['in']}:{c['out']},setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={fps},setsar=1[v{i}]")
    fc.append(f"[{i}:a]atrim={c['in']}:{c['out']},asetpts=PTS-STARTPTS,aresample=48000[a{i}]")
    labels += f"[v{i}][a{i}]"
n = len(e["clips"])
fc.append(f"{labels}concat=n={n}:v=1:a=1[vc][ac]")
vout = "[vc]"
if e.get("captions_ass"):
    ass = rp(e["captions_ass"]).replace("\\", "/").replace(":", "\\:")
    fc.append(f"[vc]ass='{ass}'[vcap]"); vout = "[vcap]"
aout = "[ac]"
if e.get("music"):
    inputs += ["-i", rp(e["music"])]; m = n
    fc.append(f"[{m}:a]volume={e.get('music_db',-18)}dB[mus]")
    fc.append("[ac]asplit=2[ac1][ac2]")
    fc.append("[mus][ac1]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=300[duck]")
    fc.append("[ac2][duck]amix=inputs=2:duration=first:normalize=0[amix]"); aout = "[amix]"
fc.append(f"{aout}loudnorm=I=-14:TP=-1.5:LRA=11[afinal]")
cmd = ["ffmpeg","-y","-loglevel","error","-stats",*inputs,"-filter_complex",";".join(fc),
       "-map",vout,"-map","[afinal]","-c:v","libx264","-preset","fast" if a.preview else "slow",
       "-crf","26" if a.preview else "17","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart",a.out]
subprocess.run(cmd, check=True); print("rendered", a.out)
