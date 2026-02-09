def total_minutes(log_file="workout_log.txt"):
    total = 0.0
    try:
        with open(log_file, "r") as file:
            for line in file:
                if "Workout duration:" in line:
                    try:
                        minutes = float(line.split("Workout duration:")[1].split("minutes")[0].strip())
                        total += minutes
                    except:
                        continue
        print(f"🧮 Total workout time logged: {round(total, 2)} minutes")
    except FileNotFoundError:
        print("⚠️ workout_log.txt not found.")

total_minutes()
