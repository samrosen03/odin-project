from datetime import datetime

def log_multiple_exercises(log_file="workout_log.txt"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print("💪 Type 'done' to finish logging.")

    entries = []
    while True:
        exercise = input("🏋️ Exercise: ").strip()
        if exercise.lower() == "done":
            break
        reps = input("🔢 Reps: ").strip()
        note = input("📝 Notes (optional): ").strip()

        if exercise and reps:
            entry = f"{now} - {exercise}: {reps}"
            if note:
                entry += f" | Note: {note}"
            entries.append(entry)

    if entries:
        with open(log_file, "a") as file:
            for entry in entries:
                file.write(entry + "\n")
        print("✅ All workouts logged!")

log_multiple_exercises()
