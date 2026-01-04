def read_dates():
    from datetime import datetime
    valid_dates = []

    try:
        with open("workout_log.txt", "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    # Try parsing first 10 characters as a date
                    date_part = line[:10]
                    dt = datetime.strptime(date_part, "%Y-%m-%d").date()
                    valid_dates.append(dt)
                except ValueError:
                    continue  # Skip lines that don’t start with a date
    except FileNotFoundError:
        print("❌ No workout_log.txt found.")
    
    return sorted(set(valid_dates))

