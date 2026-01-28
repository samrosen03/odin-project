def list_unique_exercises(log_file="workout_log.txt"):
    exercises = set()
    try:
        with open(log_file, "r") as file:
            for line in file:
                if " - " not in line:
                    continue
                _, data = line.strip().split(" - ", 1)
                for item in data.split(","):
                    if ":" in item:
                        name, _ = item.strip().split(":")
                        exercises.add(name.strip())

        print("🏋️ Unique Exercises Logged:")
        for ex in sorted(exercises):
            print(f"• {ex}")
    except FileNotFoundError:
        print("⚠️ workout_log.txt not found.")

list_unique_exercises()
