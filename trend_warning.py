from datetime import datetime
from collections import defaultdict

def detect_decline(log_file="workout_log.txt"):
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

        sorted_days = sorted(daily_totals.items())

        if len(sorted_days) < 3:
            print("Not enough data for trend detection.")
            return

        last_three = sorted_days[-3:]
        reps = [day[1] for day in last_three]

        print("\n📊 Last 3 Workout Totals:")
        for date, total in last_three:
            print(f"{date.date()} → {total} reps")

        if reps[0] > reps[1] > reps[2]:
            print("\n⚠️ WARNING: Performance declining 3 sessions in a row.")
        else:
            print("\n🔥 No consistent decline detected.")

    except FileNotFoundError:
        print("⚠️ workout_log.txt not found.")

detect_decline()