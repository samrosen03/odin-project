def average_reps(log_file="workout_log.txt"):
    date_totals = {}

    try:
        with open(log_file, "r") as file:
            for line in file:
                if " - " not in line:
                    continue
                date, data = line.strip().split(" - ", 1)
                exercises = data.split(",")
                total_reps = 0

                for item in exercises:
                    parts = item.strip().split(":")
                    if len(parts) == 2:
                        try:
                            reps = int(parts[1].strip())
                            total_reps += reps
                        except ValueError:
                            continue

                date_totals[date] = total_reps

        if date_totals:
            print("📊 Reps Per Workout Day:\n")
            for d in sorted(date_totals):
                print(f"{d}: {date_totals[d]} reps")

            avg = sum(date_totals.values()) / len(date_totals)
            print(f"\n✅ Average reps per workout: {avg:.2f}")
        else:
            print("📭 No valid data found.")

    except FileNotFoundError:
        print("❌ workout_log.txt not found.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

average_reps()
