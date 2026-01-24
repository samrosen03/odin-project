def log_new_workout(log_file="workout_log.txt"):
    from datetime import datetime

    date = datetime.now().strftime("%Y-%m-%d")
    print("📅 Logging workout for today:", date)

    entries = []
    while True:
        exercise = input("🏋️ Exercise name (or press ENTER to finish): ").strip()
        if not exercise:
            break
        reps = input(f"➕ Reps for {exercise}: ").strip()
        entries.append(f"{exercise}: {reps}")

    if entries:
        line = f"{date} - {', '.join(entries)}\n"
        with open(log_file, "a") as f:
            f.write(line)
        print("✅ Workout logged successfully!")
    else:
        print("⚠️ No exercises entered.")

log_new_workout()
