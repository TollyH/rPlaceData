ffmpeg -f image2 -framerate 120 -i "images/%09d.bmp" -c:v libx264 -crf 24 -pix_fmt yuv420p -vf "scale=1920:-1:flags=neighbor" "$1"
