from datetime import datetime
from collections import defaultdict

def rolling_average(log_file="workout_log.txt"):
    daily_totals = defaultdict(int)

    try:
        with open(log_file, "r") as f:
            for line in f:
                if " - " not in line:
                    continue

                date_str, data = line.strip().split(" - ", 1)

                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                except:
                    continue

                if ":" not in data:
                    continue

                name, reps_str = data.split(":", 1)

                try:
                    reps = int(reps_str.strip().split()[0])
                except:
                    continue

                daily_totals[date_obj] += reps

        if not daily_totals:
            print("No valid workout data found.")
            return

        sorted_days = sorted(daily_totals.items())

        last_7 = sorted_days[-7:]

        total_reps = sum(day[1] for day in last_7)
        avg = total_reps / len(last_7)

        print("\n📊 Last 7 Workout Days:")
        for date, reps in last_7:
            print(f"{date.date()} → {reps} reps")

        print(f"\n🔥 7-Day Rolling Average: {round(avg, 2)} reps")

    except FileNotFoundError:
        print("⚠️ workout_log.txt not found.")

rolling_average()
