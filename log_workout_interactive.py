def log_workout():
    date = input("📅 Enter the date (YYYY-MM-DD): ").strip()
    workout = input("🏋️ Enter workout (e.g. Pushups: 30, Squats: 40): ").strip()

    try:
        with open("workout_log.txt", "a") as file:
            file.write(f"{date} - {workout}\n")
        print("✅ Workout logged successfully!")
    except Exception as e:
        print(f"⚠️ Error: {e}")

log_workout()
