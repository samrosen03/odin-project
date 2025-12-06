from datetime import datetime

def log_workout():
    workout = input("🏋️‍♂️ Enter your workout: ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("workout_log.txt", "a") as file:
        file.write(f"[{timestamp}] {workout}\n")

    print("✅ Workout logged!")

log_workout()
