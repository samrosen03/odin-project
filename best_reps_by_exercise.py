from collections import defaultdict

def get_best_reps(log_file="workout_log.txt"):
    best = defaultdict(int)

    try:
        with open(log_file, "r") as file:
            for line in file:
                parts = line.strip().split(" - ")
                if len(parts) > 1 and ":" in parts[1]:
                    try:
                        content = parts[1].split("|")[0]
                        name, reps_info = content.split(":")
                        reps = sum(int(s) for s in reps_info.strip().split() if s.isdigit())
                        best[name.strip()] = max(best[name.strip()], reps)
                    except ValueError:
                        continue  # skip lines that don't parse cleanly

        print("🏆 Best Reps Per Exercise:")
        for exercise, max_reps in best.items():
            print(f"{exercise}: {max_reps} total reps in a session")
    except FileNotFoundError:
        print("⚠️ workout_log.txt not found.")

get_best_reps()

