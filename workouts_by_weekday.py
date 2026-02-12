from datetime import datetime
from collections import defaultdict

def count_workouts_by_day(log_file="workout_log.txt"):
    day_counts = defaultdict(int)

    try:
        with open(log_file, "r") as file:
            for line in file:
                try:
                    date_str = line.split(" - ")[0]
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    weekday = date_obj.strftime("%A")
                    day_counts[weekday] += 1
                except:
                    continue

        if day_counts:
            print("📅 Workouts per weekday:")
            for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                print(f"{day}: {day_counts[day]} sessions")
        else:
            print("No valid workout dates found.")

    except FileNotFoundError:
        print("⚠️ workout_log.txt not found.")

count_workouts_by_day()
