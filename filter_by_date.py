def filter_workouts_by_date(log_file="workout_log.txt"):
    date_query = input("🔎 Enter date to search (YYYY-MM-DD): ").strip()
    try:
        with open(log_file, "r") as file:
            found = False
            for line in file:
                if line.startswith(date_query):
                    print(f"📅 {line.strip()}")
                    found = True
            if not found:
                print("❌ No workouts found for that date.")
    except FileNotFoundError:
        print("⚠️ workout_log.txt not found.")

filter_workouts_by_date()
