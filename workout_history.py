from collections import defaultdict

log = defaultdict(list)

try:
    with open("workout_log.txt", "r") as file:
        for line in file:
            if " | " in line:
                date, data = line.strip().split(" | ", 1)
                log[date].append(data.strip())

    if log:
        print("📅 Workout History:")
        for date in sorted(log):
            print(f"\n{date}")
            for entry in log[date]:
                print(f"  - {entry}")
    else:
        print("No workouts found.")

except FileNotFoundError:
    print("❌ 'workout_log.txt' not found.")
