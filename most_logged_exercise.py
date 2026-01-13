from collections import defaultdict

def most_logged(log_file="workout_log.txt"):
    count = defaultdict(int)

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
                        count[name] += 1

        if count:
            most_common = max(count.items(), key=lambda x: x[1])
            print(f"🏆 Most Logged Exercise: {most_common[0]} ({most_common[1]} times)")
        else:
            print("📭 No valid exercise data found.")

    except FileNotFoundError:
        print("❌ workout_log.txt not found.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

most_logged()
