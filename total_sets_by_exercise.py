from collections import defaultdict

def count_total_sets(log_file="workout_log.txt"):
    totals = defaultdict(int)

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
                        name, reps_str = parts
                        reps_parts = reps_str.strip().split()
                        if len(reps_parts) >= 3 and reps_parts[1] == "sets":
                            try:
                                sets = int(reps_parts[0])
                                totals[name.strip()] += sets
                            except ValueError:
                                continue

        if totals:
            print("🏋️ Total Sets by Exercise:\n")
            for name in sorted(totals):
                print(f"{name}: {totals[name]} sets")
        else:
            print("📭 No valid set data found.")

    except FileNotFoundError:
        print("❌ workout_log.txt not found.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

count_total_sets()
