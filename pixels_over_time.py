import datetime

from matplotlib import pyplot
from tqdm import tqdm

PLACE_SECONDS_PER_LINE_POINT = 96  # 4 days = 3600 points
TOTAL_PLACEMENTS = 132224375  # Value for 2023, used for progress bar

last_placement_time = datetime.datetime(1, 1, 1)
time_since_last_point = datetime.timedelta()

graph_times: list[datetime.datetime] = []
graph_points: list[int] = []

# CSVs must be concatenated with headers removed for this program to work
with open("2023_place_canvas_history.csv", encoding="utf8") as file:
    for i, line in tqdm(enumerate(file, 1), total=TOTAL_PLACEMENTS):
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

        # Process line data
        time_since_last_point += timestamp - last_placement_time
        last_placement_time = timestamp

        if (time_since_last_point.total_seconds()
                > PLACE_SECONDS_PER_LINE_POINT):
            time_since_last_point = datetime.timedelta()
            graph_times.append(timestamp)
            graph_points.append(i)

if time_since_last_point.total_seconds() != 0:
    # There are leftover changes that didn't make it into the final point.
    # Add them now.
    graph_times.append(last_placement_time)
    graph_points.append(TOTAL_PLACEMENTS)

pyplot.plot(graph_times, graph_points)  # type: ignore
pyplot.title("Placed Pixels Over Time in r/place 2023")  # type: ignore
pyplot.ylabel("Pixels")  # type: ignore
pyplot.xlabel("Time")  # type: ignore
pyplot.savefig("pixels_over_time.png", dpi=300)  # type: ignore
