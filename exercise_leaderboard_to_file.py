from collections import defaultdict

def generate_leaderboard(log_file="workout_log.txt", output_file="leaderboard.txt"):
    exercise_totals = defaultdict(int)

    try:
        with open(log_file, "r") as file:
            for line in file:
                if " - " not in line:
                    continue
                _, data = line.strip().split(" - ", 1)
                exercises = data.split(",")

                for item in exercises:
                    parts = item.strip().split(":")
                    if len(parts) == 2:
                        name = parts[0].strip()
                        try:
                            reps = int(parts[1].strip())
                            exercise_totals[name] += reps
                        except ValueError:
                            continue

        sorted_leaderboard = sorted(exercise_totals.items(), key=lambda x: x[1], reverse=True)

        with open(output_file, "w") as out:
            out.write("🏆 Exercise Leaderboard:\n\n")
            for rank, (name, reps) in enumerate(sorted_leaderboard, 1):
                out.write(f"{rank}. {name} - {reps} reps\n")

        print(f"✅ Leaderboard saved to {output_file}")

    except FileNotFoundError:
        print("❌ workout_log.txt not found.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

generate_leaderboard()
