# volume_tracker.py

from collections import defaultdict

try:
    with open("workout_log.txt", "r") as file:
        lines = file.readlines()

    daily_totals = defaultdict(lambda: {"sets": 0, "reps": 0})

    for line in lines:
        parts = line.strip().split(" - ")
        if len(parts) != 2:
            continue

        date, data = parts
        try:
            sets = int(data.split("did")[1].split("sets")[0].strip())
            reps = int(data.split("sets of")[1].split("reps")[0].strip())
            daily_totals[date]["sets"] += sets
            daily_totals[date]["reps"] += sets * reps
        except:
            continue

    print("\n📊 Volume Totals by Day:")
    for date, totals in daily_totals.items():
        print(f"{date} → {totals['sets']} sets, {totals['reps']} total reps")

except FileNotFoundError:
    print("No workout_log.txt file found. Log some workouts first.")
