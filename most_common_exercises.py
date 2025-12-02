from collections import Counter

exercise_counter = Counter()

try:
    with open("workout_log.txt", "r") as file:
        for line in file:
            words = line.lower().split()
            for word in words:
                if word.endswith("s") and word.isalpha():  # crude filter for exercise names
                    exercise_counter[word] += 1

    print("\n📊 Most Common Exercises:")
    for exercise, count in exercise_counter.most_common(5):
        print(f"{exercise.capitalize()}: {count} entries")

except FileNotFoundError:
    print("No workout log found. Start logging workouts first!")
