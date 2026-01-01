from datetime import date

def log_workout_with_notes():
    today = date.today().isoformat()
    exercises = input("Enter your exercises (e.g., Pushups:20, Squats:30): ").strip()
    notes = input("Any notes about today’s workout? ").strip()

    log_entry = f"{today} - {exercises}"
    if notes:
        log_entry += f" | Notes: {notes}"

    with open("workout_log.txt", "a") as file:
        file.write(log_entry + "\n")

    print("✅ Workout + notes logged!")

log_workout_with_notes()
