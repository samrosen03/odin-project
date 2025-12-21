from collections import Counter

def top_exercises(log_file):
    try:
        with open(log_file, "r") as file:
            lines = file.readlines()

        all_exercises = []
        for line in lines:
            if "-" in line:
                parts = line.strip().split("-")
                if len(parts) > 1:
                    exercises = parts[1].strip().split(",")
                    for ex in exercises:
                        all_exercises.append(ex.strip().capitalize())

        count = Counter(all_exercises)
        top_three = count.most_common(3)

        print("🏆 Top 3 Most Logged Exercises:")
        for i, (exercise, reps) in enumerate(top_three, 1):
            print(f"{i}. {exercise} - {reps} times")
    except FileNotFoundError:
        print("❌ No workout log found.")

top_exercises("workout_log.txt")
