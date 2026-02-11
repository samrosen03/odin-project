from datetime import datetime

def log_workout():
    date = datetime.now().strftime("%Y-%m-%d")
    workout = input("🏋️ Exercise performed: ")
    reps = input("🔁 Sets/Reps (e.g. 4 sets of 10): ")
    note = input("🗒️ Any notes? ")

    entry = f"{date} - {workout}: {reps} | Note: {note}\n"

    with open("workout_log.txt", "a") as file:
        file.write(entry)

    print("✅ Workout logged with note!")

log_workout()
