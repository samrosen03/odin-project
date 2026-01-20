from collections import defaultdict
from datetime import datetime

def count_workouts_per_month(log_file="workout_log.txt"):
    monthly_counts = defaultdict(int)

    try:
        with open(log_file, "r") as file:
            for line in file:
                if " - " not in line:
                    continue
                date_str, _ = line.strip().split(" - ", 1)
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    month_year = date_obj.strftime("%B %Y")  # e.g. "January 2024"
                    monthly_counts[month_year] += 1
                except ValueError:
                    continue

        if monthly_counts:
            print("📆 Workouts Per Month:\n")
            for month in sorted(monthly_counts):
                print(f"{month}: {monthly_counts[month]} workout(s)")
        else:
            print("📭 No valid entries found.")

    except FileNotFoundError:
        print("❌ workout_log.txt not found.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

count_workouts_per_month()
