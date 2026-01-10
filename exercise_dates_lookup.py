def lookup_exercise_dates(target, log_file="workout_log.txt"):
    target = target.strip().lower()
    matching_dates = []

    try:
        with open(log_file, "r") as file:
            for line in file:
                if " - " not in line:
                    continue
                date_str, data = line.strip().split(" - ", 1)
                exercises = data.split(",")

                for item in exercises:
                    parts = item.strip().split(":")
                    if len(parts) == 2:
                        name = parts[0].strip().lower()
                        if name == target:
                            matching_dates.append(date_str)

        if matching_dates:
            print(f"📆 You logged '{target.title()}' on these days:\n")
            for d in matching_dates:
                print(f"• {d}")
        else:
            print(f"❌ No logs found for '{target.title()}'.")

    except FileNotFoundError:
        print("❌ workout_log.txt not found.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

# 👇 Replace this with any exercise you want to look up!
lookup_exercise_dates("Pushups")
