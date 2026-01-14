def show_recent_workouts(log_file="workout_log.txt", n=5):
    try:
        with open(log_file, "r") as file:
            lines = file.readlines()
            recent = lines[-n:]

        print(f"🕒 Last {len(recent)} Workouts:\n")
        for line in recent:
            print(f"• {line.strip()}")

    except FileNotFoundError:
        print("❌ workout_log.txt not found.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

show_recent_workouts()
