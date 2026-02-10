def average_duration(log_file="workout_log.txt"):
    total = 0.0
    count = 0

    try:
        with open(log_file, "r") as file:
            for line in file:
                if "Workout duration:" in line:
                    try:
                        minutes = float(line.split("Workout duration:")[1].split("minutes")[0].strip())
                        total += minutes
                        count += 1
                    except:
                        continue
        if count > 0:
            average = round(total / count, 2)
            print(f"📊 Average workout time: {average} minutes over {count} sessions")
        else:
            print("📭 No workout durations found.")
    except FileNotFoundError:
        print("⚠️ workout_log.txt not found.")

average_duration()
