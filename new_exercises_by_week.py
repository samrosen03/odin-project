from datetime import datetime
from collections import defaultdict

def track_new_exercises(log_file="workout_log.txt"):
    week_to_exercises = defaultdict(set)
    seen_exercises = set()

    try:
        with open(log_file, "r") as file:
            for line in file:
                if " - " not in line:
                    continue
                date_str, data = line.strip().split(" - ", 1)
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    continue

                week = f"{date_obj.isocalendar()[1]}-{date_obj.year}"
                exercises = data.split(",")

                for item in exercises:
                    parts = item.strip().split(":")
                    if len(parts) == 2:
                        name = parts[0].strip()
                        if name not in seen_exercises:
                            week_to_exercises[week].add(name)
                            seen_exercises.add(name)

        if not week_to_exercises:
            print("📭 No new exercises found.")
            return

        print("📈 New Exercises Introduced by Week:\n")
        for week in sorted(week_to_exercises):
            new_list = sorted(week_to_exercises[week])
            print(f"Week {week}: {len(new_list)} new exercise(s) — {', '.join(new_list)}")

    except FileNotFoundError:
        print("❌ workout_log.txt not found.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

track_new_exercises()
