def reps_by_day():
    target_date = input("Enter a date (YYYY-MM-DD): ").strip()
    total_reps = 0

    try:
        with open("workout_log.txt", "r") as file:
            for line in file:
                if line.startswith(target_date):
                    parts = line.strip().split(" - ")
                    if len(parts) >= 2:
                        details = parts[1]
                        reps = int(details.split(":")[1].strip())
                        total_reps += reps

        print(f"🗓️ Total reps on {target_date}: {total_reps}")
    except FileNotFoundError:
        print("❌ workout_log.txt not found.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

reps_by_day()
