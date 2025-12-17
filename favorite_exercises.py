from collections import Counter

def favorite_exercises(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        exercises = []
        for line in lines:
            if "-" in line:
                parts = line.strip().split(" - ")
                if len(parts) > 1:
                    workouts = parts[1].split(",")
                    for workout in workouts:
                        name = workout.strip().split(":")[0].strip().lower()
                        exercises.append(name)
        count = Counter(exercises)
        top_3 = count.most_common(3)
        print("🏆 Top 3 Favorite Exercises:")
        for i, (exercise, times) in enumerate(top_3, 1):
            print(f"{i}. {exercise.title()} — {times} times")
    except FileNotFoundError:
        print("❌ workout_log.txt not found.")

favorite_exercises("workout_log.txt")
