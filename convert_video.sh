ffmpeg -i "$1" \
  -vf "scale=-2:720" \
  -c:a aac \
  -c:v libx264 -profile:v high -level:v 3.1 \
  -x264opts scenecut=0:open_gop=0:min-keyint=72:keyint=72 \
  -b:v 1000k -maxrate 1000k -bufsize 1500k \
  -b:a 64k \
  -pass 1 -f mp4 /dev/null

 ffmpeg -i "$1" \
  -vf "scale=-2:720" \
  -c:a aac \
  -c:v libx264 -profile:v high -level:v 3.1 \
  -x264opts scenecut=0:open_gop=0:min-keyint=72:keyint=72 \
  -b:v 1000k -maxrate 1000k -bufsize 1500k \
  -b:a 64k \
  -pass 2 \
  -y ./video_output/$2.mp4
