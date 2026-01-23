from collections import defaultdict

def count_reps(log_file="workout_log.txt"):
    totals = defaultdict(int)

    try:
        with open(log_file, "r") as file:
            for line in file:
                if " - " not in line:
                    continue
                _, data = line.strip().split(" - ", 1)
                for item in data.split(","):
                    if ":" in item:
                        name, reps = item.strip().split(":")
                        try:
                            totals[name.strip()] += int(reps.strip())
                        except ValueError:
                            continue

        print("💪 Total Reps Logged:\n")
        for name, total in totals.items():
            print(f"• {name}: {total}")
    except FileNotFoundError:
        print("❌ workout_log.txt not found.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

count_reps()
