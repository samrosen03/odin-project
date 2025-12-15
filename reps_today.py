from datetime import date

today = date.today().isoformat()  # format: YYYY-MM-DD
total_reps = 0

try:
    with open("workout_log.txt", "r") as file:
        for line in file:
            if line.startswith(today):
                parts = line.strip().split("|")
                if len(parts) > 1:
                    exercises = parts[1].split(",")
                    for ex in exercises:
                        _, reps = ex.strip().split()
                        total_reps += int(reps)
except FileNotFoundError:
    print("Log file not found.")

print(f"🔥 Total reps for today ({today}): {total_reps}")
