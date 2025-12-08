import re
from collections import defaultdict

totals = defaultdict(int)

try:
    with open("workout_log.txt", "r") as file:
        for line in file:
            entries = line.strip().split(",")
            for entry in entries:
                match = re.match(r"(\w+)\s+(\d+)", entry.strip())
                if match:
                    exercise = match.group(1).capitalize()
                    reps = int(match.group(2))
                    totals[exercise] += reps

    if totals:
        most_trained = max(totals, key=totals.get)
        print(f"🏆 Most trained exercise: {most_trained} with {totals[most_trained]} reps")
    else:
        print("No workouts found.")

except FileNotFoundError:
    print("❌ 'workout_log.txt' not found.")
