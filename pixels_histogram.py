import datetime

from matplotlib import pyplot
from tqdm import tqdm

PLACE_SECONDS_PER_LINE_POINT = 96  # 4 days = 3600 points
TOTAL_PLACEMENTS = 160353104  # Value for 2022, used for progress bar

graph_points: list[datetime.datetime] = []

# CSV must be pre-sorted with header removed for this program to work
with open("2022_place_canvas_history.sorted.csv", encoding="utf8") as file:
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
        graph_points.append(timestamp)

print("Generating histogram...")
pyplot.hist(graph_points, bins=96)  # type: ignore
pyplot.title("Placed Pixels By Time in r/place 2022")  # type: ignore
pyplot.ylabel("Pixels")  # type: ignore
pyplot.xlabel("Time")  # type: ignore
pyplot.savefig("pixels_histogram.png", dpi=300)  # type: ignore
