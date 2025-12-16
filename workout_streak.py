from datetime import datetime, timedelta

def read_workout_dates(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        dates = set()
        for line in lines:
            if line.strip():
                date_str = line.split(" - ")[0].strip()
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    dates.add(date)
                except ValueError:
                    continue
        return sorted(dates, reverse=True)
    except FileNotFoundError:
        print("No workout log found.")
        return []

def calculate_streak(dates):
    if not dates:
        return 0

    streak = 1
    today = datetime.today().date()
    for i in range(1, len(dates)):
        if dates[i] == dates[i-1] - timedelta(days=1):
            streak += 1
        else:
            break
    return streak

dates = read_workout_dates("workout_log.txt")
streak = calculate_streak(dates)

print(f"🔥 Current workout streak: {streak} day(s)")
