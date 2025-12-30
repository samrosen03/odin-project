def filter_high_rep_workouts(min_reps=20, log_file="workout_log.txt"):
    try:
        with open(log_file, "r") as file:
            for line in file:
                parts = line.strip().split(" - ")
                if len(parts) < 2:
                    continue

                date = parts[0]
                exercises = parts[1].split(",")

                high_rep = []
                for ex in exercises:
                    try:
                        name, reps = ex.strip().split(":")
                        if int(reps) >= min_reps:
                            high_rep.append(f"{name.strip()} ({reps} reps)")
                    except ValueError:
                        continue

                if high_rep:
                    print(f"{date}: {' | '.join(high_rep)}")

    except FileNotFoundError:
        print("❌ workout_log.txt not found.")

filter_high_rep_workouts()
