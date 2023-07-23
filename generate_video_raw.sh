ffmpeg -f image2 -framerate 60 -i "images/%09d.bmp" -c:v libx264 -qp 0 -pix_fmt yuvj444p "$1"
