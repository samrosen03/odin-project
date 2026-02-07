from collections import Counter

def most_common_exercise(log_file="workout_log.txt"):
    exercises = []

    try:
        with open(log_file, "r") as file:
            for line in file:
                parts = line.strip().split(" - ")
                if len(parts) > 1 and ":" in parts[1]:
                    try:
                        name = parts[1].split(":")[0].strip()
                        exercises.append(name)
                    except:
                        continue

        if exercises:
            count = Counter(exercises)
            top = count.most_common(1)[0]
            print(f"🏆 Most Frequently Logged: {top[0]} ({top[1]} times)")
        else:
            print("📭 No exercises found in log.")
    except FileNotFoundError:
        print("⚠️ workout_log.txt not found.")

most_common_exercise()
