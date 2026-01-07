from datetime import datetime
from collections import defaultdict

def summarize_weekly_workouts(log_file="workout_log.txt"):
    weekly_totals = defaultdict(int)

    try:
        with open(log_file, "r") as file:
            for line in file:
                if not line.strip() or " - " not in line:
                    continue

                date_str = line.split(" - ")[0].strip()
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    year, week_num, _ = date_obj.isocalendar()
                    weekly_totals[f"Week {week_num}, {year}"] += 1
                except ValueError:
                    continue

        if not weekly_totals:
            print("📭 No valid workout entries found.")
            return

        print("📅 Weekly Workout Summary:\n")
        for week in sorted(weekly_totals):
            print(f"{week}: {weekly_totals[week]} workout(s)")

    except FileNotFoundError:
        print("❌ workout_log.txt not found.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

summarize_weekly_workouts()

