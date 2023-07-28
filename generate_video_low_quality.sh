ffmpeg -f image2 -framerate 60 -i "images/%09d.bmp" -c:v libx264 -crf 24 -pix_fmt yuv420p -vf "scale=-1:500" "$1"
