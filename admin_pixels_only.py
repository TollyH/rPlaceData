import datetime
import os

import numpy
from numpy.typing import NDArray
from PIL import Image
from skimage.draw import disk
from tqdm import tqdm

CANVAS_SIZE = (3000, 2000)
X_OFFSET = 1500
Y_OFFSET = 1000
PLACE_SECONDS_PER_VIDEO_FRAMES = 96  # 4 days = 3600 frames (60s at 60 fps)
TOTAL_PLACEMENTS = 132224375  # Value for 2023, used for progress bar

# 2D array of pixels
canvas: NDArray[numpy.uint8] = numpy.array(
    [
        [(255, 255, 255)] * CANVAS_SIZE[0]
        for _ in range(CANVAS_SIZE[1])
    ],
    dtype=numpy.uint8
)
images_saved = 0

last_placement_time = datetime.datetime(1, 1, 1)
time_since_last_frame = datetime.timedelta()

if not os.path.exists("images"):
    os.mkdir("images")

# CSVs must be concatenated with headers removed for this program to work
with open("2023_place_canvas_history.csv", encoding="utf8") as file:
    for line in tqdm(file, total=TOTAL_PLACEMENTS):
        # Parse line data
        split = line.replace('"', '').split(",")
        if len(split[0]) == 23:
            timestamp = datetime.datetime.strptime(
                split[0], "%Y-%m-%d %H:%M:%S UTC"
            )
        else:
            timestamp = datetime.datetime.strptime(
                split[0], "%Y-%m-%d %H:%M:%S.%f UTC"
            )
        user_id = split[1]
        if len(split) == 7:
            # Admin rectangle drawing tool
            coordinate = (
                int(split[2]) + X_OFFSET, int(split[3]) + Y_OFFSET,
                int(split[4]) + X_OFFSET, int(split[5]) + Y_OFFSET
            )
            admin_rect = True
        elif len(split) == 6:
            # Admin circle drawing tool
            coordinate = (
                int(split[2][3:]) + X_OFFSET, int(split[3][3:]) + Y_OFFSET,
                int(split[4][3:-1])
            )
            admin_rect = False
        else:
            continue
        # Convert hex string to tuple of three 0..255 values
        color = tuple(int(split[-1][i + 1:i + 3], 16) for i in (0, 2, 4))

        # Process line data
        time_since_last_frame += timestamp - last_placement_time
        last_placement_time = timestamp

        if admin_rect:
            assert len(coordinate) == 4
            canvas[
                coordinate[1]:coordinate[3] + 1,
                coordinate[0]:coordinate[2] + 1
            ] = color
        else:
            assert len(coordinate) == 3
            circle = disk(  # type: ignore
                (coordinate[1], coordinate[0]), coordinate[2])
            canvas[circle] = color

        if (time_since_last_frame.total_seconds()
                > PLACE_SECONDS_PER_VIDEO_FRAMES):
            time_since_last_frame = datetime.timedelta()
            image = Image.fromarray(canvas, "RGB")  # type: ignore
            image.save(os.path.join("images", f"{images_saved:09d}.bmp"))
            images_saved += 1

if time_since_last_frame.total_seconds() != 0:
    # There are leftover changes that didn't make it into the final frame.
    # Save them now.
    image = Image.fromarray(canvas, "RGB")  # type: ignore
    image.save(os.path.join("images", f"{images_saved:09d}.bmp"))
    images_saved += 1
