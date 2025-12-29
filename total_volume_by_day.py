from collections import defaultdict

def calculate_volume_by_day(log_file="workout_log.txt"):
    volume = defaultdict(int)

    try:
        with open(log_file, "r") as file:
            for line in file:
                parts = line.strip().split(" - ")
                if len(parts) < 2:
                    continue

                date = parts[0]
                exercises = parts[1].split(",")

                for ex in exercises:
                    try:
                        name, reps = ex.strip().split(":")
                        volume[date] += int(reps)
                    except ValueError:
                        continue

        for date, total in sorted(volume.items()):
            print(f"{date}: {total} total reps")
    except FileNotFoundError:
        print("❌ workout_log.txt not found.")

calculate_volume_by_day()
