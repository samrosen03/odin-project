def count_unique_exercises(log_file="workout_log.txt"):
    unique_exercises = set()

    try:
        with open(log_file, "r") as file:
            for line in file:
                if " - " not in line:
                    continue
                _, data = line.strip().split(" - ", 1)
                exercises = data.split(",")

                for item in exercises:
                    parts = item.strip().split(":")
                    if len(parts) == 2:
                        name = parts[0].strip()
                        unique_exercises.add(name)

        print(f"🧠 You've logged {len(unique_exercises)} unique exercises:")
        for ex in sorted(unique_exercises):
            print(f"• {ex}")

    except FileNotFoundError:
        print("❌ workout_log.txt not found.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

count_unique_exercises()
