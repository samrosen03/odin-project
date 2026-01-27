from datetime import datetime

def log_workout_with_time(log_file="workout_log.txt"):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")

    exercise = input("🏋️ Exercise: ").strip()
    reps = input("➕ Reps: ").strip()

    if exercise and reps:
        entry = f"{date_str} {time_str} - {exercise}: {reps}\n"
        with open(log_file, "a") as file:
            file.write(entry)
        print("✅ Workout logged!")
    else:
        print("⚠️ Missing input.")

log_workout_with_time()
