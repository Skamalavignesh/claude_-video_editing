#!/usr/bin/env bash
# Technical QA of a finished reel. Usage: qa_check.sh <reel.mp4>
f="$1"
echo "== $f"
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt -of default=nw=1 "$f"
D=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$f"); echo "duration: $D s"
W=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$f"); H=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$f")
[ "$W" = 1080 ] && [ "$H" = 1920 ] && echo "[ok] 1080x1920" || echo "[!!] not 1080x1920 (${W}x${H})"
awk "BEGIN{exit !($D<=90)}" && echo "[ok] <= 90s" || echo "[!!] longer than 90s"
ffmpeg -hide_banner -i "$f" -af loudnorm=print_format=summary -f null - 2>&1 | grep -E "Input Integrated|Input True Peak"
echo "black frames:"; ffmpeg -hide_banner -i "$f" -vf blackdetect=d=0.2 -an -f null - 2>&1 | grep black_start || echo "  none"
