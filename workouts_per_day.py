from collections import defaultdict

def count_workouts_per_day(log_file="workout_log.txt"):
    counts = defaultdict(int)

    try:
        with open(log_file, "r") as file:
            for line in file:
                if " - " in line:
                    date = line.split(" - ")[0].split(" ")[0]
                    counts[date] += 1

        print("📅 Workouts Per Day:")
        for date in sorted(counts):
            print(f"{date}: {counts[date]} workout(s)")
    except FileNotFoundError:
        print("⚠️ workout_log.txt not found.")

count_workouts_per_day()
