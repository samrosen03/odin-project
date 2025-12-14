best_sets = {}

with open("workout_log.txt", "r") as file:
    for line in file:
        parts = line.strip().split("|")
        if len(parts) < 2:
            continue
        exercises = parts[1].split(",")
        for ex in exercises:
            name, reps = ex.strip().split()
            reps = int(reps)
            if name not in best_sets or reps > best_sets[name]:
                best_sets[name] = reps

print("💪 Best Set Per Exercise:")
for name, reps in best_sets.items():
    print(f"{name}: {reps} reps")
