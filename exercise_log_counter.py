from collections import defaultdict

def count_exercise_logs(log_file="workout_log.txt"):
    counts = defaultdict(int)

    try:
        with open(log_file, "r") as file:
            for line in file:
                if " - " not in line:
                    continue
                _, data = line.strip().split(" - ", 1)
                for item in data.split(","):
                    if ":" in item:
                        name, _ = item.strip().split(":")
                        counts[name.strip()] += 1

        print("📊 Exercise Log Count:")
        for name, count in sorted(counts.items()):
            print(f"• {name}: {count} times")
    except FileNotFoundError:
        print("⚠️ workout_log.txt not found.")

count_exercise_logs()
