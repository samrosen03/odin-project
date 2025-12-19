from datetime import datetime, timedelta

def summarize_week(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        today = datetime.now()
        week_ago = today - timedelta(days=7)

        workouts_this_week = []

        for line in lines:
            if "-" in line:
                date_str = line.split(" - ")[0].strip()
                try:
                    workout_date = datetime.strptime(date_str, "%Y-%m-%d")
                    if week_ago.date() <= workout_date.date() <= today.date():
                        workouts_this_week.append(workout_date.strftime("%A"))
                except ValueError:
                    pass  # Skip lines with bad date formatting

        if workouts_this_week:
            print(f"✅ You trained {len(workouts_this_week)} times in the past 7 days.")
            print("📅 Days trained:", ", ".join(sorted(set(workouts_this_week))))
        else:
            print("❌ No workouts logged in the past 7 days.")

    except FileNotFoundError:
        print("workout_log.txt not found.")

summarize_week("workout_log.txt")
