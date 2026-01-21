def list_exercises(log_file="workout_log.txt"):
    exercises = set()

    try:
        with open(log_file, "r") as file:
            for line in file:
                if " - " not in line:
                    continue
                _, data = line.strip().split(" - ", 1)
                for pair in data.split(","):
                    name = pair.strip().split(":")[0].strip()
                    exercises.add(name)

        if exercises:
            print("🏋️ Unique Exercises You've Logged:")
            for ex in sorted(exercises):
                print(f"• {ex}")
        else:
            print("📭 No exercises found.")
    except FileNotFoundError:
        print("❌ workout_log.txt not found.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

list_exercises()
