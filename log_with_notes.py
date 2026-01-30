from datetime import datetime

def log_workout_with_notes(log_file="workout_log.txt"):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M")

    exercise = input("🏋️ Exercise: ").strip()
    reps = input("🔢 Reps: ").strip()
    note = input("📝 Notes (optional): ").strip()

    if exercise and reps:
        entry = f"{date_str} - {exercise}: {reps}"
        if note:
            entry += f" | Note: {note}"
        entry += "\n"

        with open(log_file, "a") as file:
            file.write(entry)

        print("✅ Workout + Note logged!")
    else:
        print("⚠️ Missing required fields.")

log_workout_with_notes()
