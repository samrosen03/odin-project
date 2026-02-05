from collections import defaultdict

def group_workouts(log_file="workout_log.txt"):
    grouped = defaultdict(list)

    try:
        with open(log_file, "r") as file:
            for line in file:
                parts = line.strip().split(" - ")
                if len(parts) > 1 and ":" in parts[1]:
                    exercise, rest = parts[1].split(":", 1)
                    grouped[exercise.strip()].append(line.strip())

        for exercise, logs in grouped.items():
            print(f"\n🏋️ {exercise} ({len(logs)} entries)")
            for entry in logs:
                print(f"  - {entry}")
    except FileNotFoundError:
        print("⚠️ workout_log.txt not found.")

group_workouts()
