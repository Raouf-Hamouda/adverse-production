#!/bin/zsh
# Re-encodes media/web/*.mp4 into: <name>.av1.mp4 (desktop, Chrome/Firefox/Edge), <name>.p.av1.mp4 / <name>.p.hevc.mp4 / <name>.p.mp4 (phone, 960 wide). Original mp4 stays = desktop fallback.
cd "$(dirname "$0")/media/web" || exit 1
for f in *.mp4; do
  case $f in *.av1.mp4|*.p.mp4|*.p.hevc.mp4|*.p.av1.mp4) continue;; esac
  b=${f%.mp4}
  [ -f $b.av1.mp4 ]    || ffmpeg -y -v error -i $f -an -c:v libsvtav1 -preset 5 -crf 34 -g 240 -svtav1-params tune=0 -pix_fmt yuv420p -movflags +faststart $b.av1.mp4
  [ -f $b.p.av1.mp4 ]  || ffmpeg -y -v error -i $f -an -vf scale=960:-2 -c:v libsvtav1 -preset 5 -crf 36 -g 240 -svtav1-params tune=0 -pix_fmt yuv420p -movflags +faststart $b.p.av1.mp4
  [ -f $b.p.hevc.mp4 ] || ffmpeg -y -v error -i $f -an -vf scale=960:-2 -c:v libx265 -preset medium -crf 26 -tag:v hvc1 -pix_fmt yuv420p -movflags +faststart -x265-params log-level=error $b.p.hevc.mp4
  [ -f $b.p.mp4 ]      || ffmpeg -y -v error -i $f -an -vf scale=960:-2 -c:v libx264 -preset slow -crf 26 -profile:v high -pix_fmt yuv420p -movflags +faststart $b.p.mp4
  echo "done $b"
done
