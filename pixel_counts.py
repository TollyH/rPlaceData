from tqdm import tqdm

CANVAS_SIZE = (3000, 2000)
X_OFFSET = 1500
Y_OFFSET = 1000
TOTAL_PLACEMENTS = 132224375  # Value for 2023, used for progress bar

# Does not include admin rect updates
pixel_update_counts: dict[tuple[int, int], int] = {
    (x, y): 0 for x in range(CANVAS_SIZE[0]) for y in range(CANVAS_SIZE[1])
}

# CSVs must be concatenated with headers removed for this program to work
with open("2023_place_canvas_history.csv", encoding="utf8") as file:
    for line in tqdm(file, total=TOTAL_PLACEMENTS):
        split = line.replace('"', '').split(",")
        # Exclude admin rectangles
        if len(split) == 5:
            coordinate = (int(split[2]) + X_OFFSET, int(split[3]) + Y_OFFSET)
            pixel_update_counts[coordinate] += 1

pixel_counts_text = '\n'.join(
    f"{x},{y},{c}" for (x, y), c in pixel_update_counts.items()
)
with open("pixel_updates_counts.csv", 'w', encoding="utf8") as file:
    file.write(pixel_counts_text)
