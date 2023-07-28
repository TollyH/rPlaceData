import math

import numpy
from numpy.typing import NDArray
from PIL import Image
from tqdm import tqdm

CANVAS_SIZE = (3000, 2000)
X_OFFSET = 1500
Y_OFFSET = 1000
PIXEL_COUNT = CANVAS_SIZE[0] * CANVAS_SIZE[1]  # Used for progress bar

COLD_COLOR = (0, 0, 255)
HOT_COLOR = (255, 0, 0)

# 2D array of pixels
canvas: NDArray[numpy.uint8] = numpy.array(
    [
        [(255, 255, 255)] * CANVAS_SIZE[0]
        for _ in range(CANVAS_SIZE[1])
    ],
    dtype=numpy.uint8
)

minimum_placements = float('inf')
maximum_placements = float('-inf')

# Does not include admin rect updates
pixel_update_counts: dict[tuple[int, int], int] = {
    (x, y): 0 for x in range(CANVAS_SIZE[0]) for y in range(CANVAS_SIZE[1])
}

print("Loading pixel counts:")
# Pixel counts script must be run before this one
with open("pixel_updates_counts.csv", encoding="utf8") as file:
    for line in tqdm(file, total=PIXEL_COUNT):
        x, y, count = (int(n) for n in line.split(','))
        if count > maximum_placements:
            maximum_placements = count
        if count < minimum_placements:
            minimum_placements = count
        pixel_update_counts[(x, y)] = count

print("Generating heatmap:")
placements_difference = maximum_placements - minimum_placements
for (x, y), count in tqdm(pixel_update_counts.items()):
    # Calculate the logarithmic proportion
    proportion = (
        math.log(count + 1) - math.log(minimum_placements + 1)
    ) / math.log(placements_difference + 1)
    # Generate the colour in-between the hot and cold color based on the
    # proportion.
    canvas[y, x] = tuple(
        int((c * (1 - proportion)) + (h * proportion))
        for h, c in zip(HOT_COLOR, COLD_COLOR)
    )

image = Image.fromarray(canvas, "RGB")  # type: ignore
image.save("heatmap.png")
