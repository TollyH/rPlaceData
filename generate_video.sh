ffmpeg -f image2 -framerate 60 -i "images/%09d.png" -c:v libx264 -crf 24 -pix_fmt yuv420p "$1"
