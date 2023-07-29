from matplotlib import pyplot
from tqdm import tqdm

TOTAL_PLACEMENTS = 132224375  # Value for 2023, used for progress bar

colors: dict[tuple[int, int, int], int] = {}

# CSVs must be concatenated with headers removed for this program to work
with open("2023_place_canvas_history.csv", encoding="utf8") as file:
    for line in tqdm(file, total=TOTAL_PLACEMENTS):
        # Parse line data
        split = line.replace('"', '').split(",")
        # Convert hex string to tuple of three 0..255 values
        color = tuple(int(split[-1][i + 1:i + 3], 16) for i in (0, 2, 4))
        if color in colors:
            colors[color] += 1
        else:
            colors[color] = 1

# Ensure colors are in the correct format and counts match up when passing to
# matplotlib
color_keys: list[tuple[float, float, float]] = []
color_values: list[int] = []
for (r, g, b), count in colors.items():
    color_keys.append((r / 255, g / 255, b / 255))
    color_values.append(count)

pyplot.pie(color_values, colors=color_keys)  # type: ignore
pyplot.title("Most Placed Colors in r/place 2023")  # type: ignore
pyplot.savefig("color_pie_chart.png", dpi=300)  # type: ignore
