exercise_counts = {}

with open("workout_log.txt", "r") as file:
    for line in file:
        parts = line.strip().split("|")
        if len(parts) < 2:
            continue
        exercises = parts[1].split(",")
        for ex in exercises:
            name = ex.strip().split()[0].capitalize()
            exercise_counts[name] = exercise_counts.get(name, 0) + 1

for name, count in exercise_counts.items():
    print(f"{name}: {count}")
