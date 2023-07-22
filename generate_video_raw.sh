ffmpeg -f image2 -framerate 60 -i "images/%09d.png" -c:v libx264 -qp 0 -pix_fmt yuvj444p "$1"
