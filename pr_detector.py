def detect_prs(log_file="workout_log.txt"):
    best = {}

    try:
        with open(log_file, "r") as file:
            for line in file:
                if " - " not in line:
                    continue

                date, data = line.strip().split(" - ", 1)

                if ":" not in data:
                    continue

                exercise, reps_str = data.split(":", 1)

                try:
                    reps = int(reps_str.strip().split()[0])
                except:
                    continue

                exercise = exercise.strip()

                if exercise not in best:
                    best[exercise] = reps
                    print(f"🔥 First PR for {exercise}: {reps} reps on {date}")
                elif reps > best[exercise]:
                    print(f"🏆 NEW PR for {exercise}! {reps} reps on {date} (Old: {best[exercise]})")
                    best[exercise] = reps

    except FileNotFoundError:
        print("⚠️ workout_log.txt not found.")

detect_prs()
