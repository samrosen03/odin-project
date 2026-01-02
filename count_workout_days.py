def count_workout_days():
    try:
        with open("workout_log.txt", "r") as file:
            lines = file.readlines()

        # Extract dates (the part before the first space or dash)
        dates = {line.split()[0] for line in lines if line.strip()}
        print(f"📅 You've worked out on {len(dates)} different days.")
    except FileNotFoundError:
        print("❌ No workout log found.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

count_workout_days()
