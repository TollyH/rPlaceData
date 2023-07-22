import os

from tqdm import tqdm

CANVAS_SIZE = (2000, 2000)
TOTAL_PLACEMENTS = 160353104  # Value for 2022, used for progress bar

# Does not include admin rect updates
pixel_update_counts: dict[tuple[int, int], int] = {
    (x, y): 0 for x in range(CANVAS_SIZE[0]) for y in range(CANVAS_SIZE[1])
}

if not os.path.exists("images"):
    os.mkdir("images")

# CSV must be pre-sorted with header removed for this program to work
with open("2022_place_canvas_history.sorted.csv", encoding="utf8") as file:
    for line in tqdm(file, total=TOTAL_PLACEMENTS):
        split = line.replace('"', '').split(",")
        # Exclude admin rectangles
        if len(split) == 5:
            coordinate = (int(split[3]), int(split[4]))
            pixel_update_counts[coordinate] += 1

pixel_counts_text = '\n'.join(
    f"{x},{y},{c}" for (x, y), c in pixel_update_counts.items()
)
with open("pixel_updates_counts.csv", 'w', encoding="utf8") as file:
    file.write(pixel_counts_text)
