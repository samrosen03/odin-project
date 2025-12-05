import re

high_intensity_count = 0

try:
    with open("workout_log.txt", "r") as file:
        for line in file:
            reps = re.findall(r'\b\d+\b', line)
            total = sum(int(num) for num in reps)
            if total > 50:
                high_intensity_count += 1

    print(f"🔥 Workouts with over 50 total reps: {high_intensity_count}")

except FileNotFoundError:
    print("Workout log not found. Start logging to get results!")
