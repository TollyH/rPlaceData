import datetime
import os

from matplotlib import pyplot
from tqdm import tqdm

CANVAS_SIZE = (2000, 2000)
PLACE_SECONDS_PER_LINE_POINT = 96  # 4 days = 3600 points
TOTAL_PLACEMENTS = 160353104  # Value for 2022, used for progress bar

last_placement_time = datetime.datetime(1, 1, 1)
time_since_last_point = datetime.timedelta()

already_seen_users: set[str] = set()
graph_times: list[datetime.datetime] = []
graph_points: list[int] = []

if not os.path.exists("images"):
    os.mkdir("images")

# CSV must be pre-sorted with header removed for this program to work
with open("2022_place_canvas_history.sorted.csv", encoding="utf8") as file:
    for line in tqdm(file, total=TOTAL_PLACEMENTS):
        # Parse line data
        split = line.replace('"', '').split(",")
        user_id = split[1]
        if user_id in already_seen_users:
            continue
        already_seen_users.add(user_id)
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
            graph_points.append(len(already_seen_users))

if time_since_last_point.total_seconds() != 0:
    # There are leftover changes that didn't make it into the final point.
    # Add them now.
    graph_times.append(last_placement_time)
    graph_points.append(len(already_seen_users))

pyplot.plot(graph_times, graph_points)  # type: ignore
pyplot.title("Unique Users Over Time in r/place 2022")  # type: ignore
pyplot.ylabel("Users")  # type: ignore
pyplot.xlabel("Time")  # type: ignore
pyplot.savefig("users_over_time.png", dpi=300)  # type: ignore
