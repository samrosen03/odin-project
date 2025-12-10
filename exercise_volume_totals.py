from collections import defaultdict

volume = defaultdict(int)

try:
    with open("workout_log.txt", "r") as file:
        for line in file:
            if " | " in line:
                _, data = line.strip().split(" | ", 1)
                exercises = data.split(",")
                for item in exercises:
                    name, reps = item.strip().rsplit(" ", 1)
                    volume[name] += int(reps)

    if volume:
        print("🏆 Total Reps by Exercise:\n")
        for exercise, reps in sorted(volume.items(), key=lambda x: -x[1]):
            print(f"{exercise}: {reps}")
    else:
        print("No exercises found in log.")

except FileNotFoundError:
    print("❌ 'workout_log.txt' not found.")
