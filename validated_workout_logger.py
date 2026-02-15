from datetime import datetime

LOG_FILE = "workout_log.txt"

def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_valid_number(value):
    return value.isdigit()

def log_workout():
    date = input("📅 Enter date (YYYY-MM-DD): ").strip()
    if not is_valid_date(date):
        print("❌ Invalid date format.")
        return

    exercise = input("🏋️ Exercise: ").strip()
    reps = input("🔢 Reps: ").strip()

    if not is_valid_number(reps):
        print("❌ Reps must be a number.")
        return

    with open(LOG_FILE, "a") as f:
        f.write(f"{date} - {exercise}: {reps}\n")

    print("✅ Workout logged successfully.")

log_workout()
