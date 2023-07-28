from tqdm import tqdm

TOTAL_PLACEMENTS = 132224375  # Value for 2023, used for progress bar

user_place_counts: dict[str, int] = {}

# CSVs must be concatenated with headers removed for this program to work
with open("2023_place_canvas_history.csv", encoding="utf8") as file:
    for line in tqdm(file, total=TOTAL_PLACEMENTS):
        split = line.replace('"', '').split(",")
        user_id = split[1]
        if user_id in user_place_counts:
            user_place_counts[user_id] += 1
        else:
            user_place_counts[user_id] = 1

user_counts_text = '\n'.join(
    f"{u},{c}" for u, c in user_place_counts.items()
)
with open("user_place_counts.csv", 'w', encoding="utf8") as file:
    file.write(user_counts_text)
