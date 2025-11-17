# multi_workout_logger.py

workouts = []

while True:
    exercise = input("Enter an exercise (or type 'done' to finish): ")
    if exercise.lower() == 'done':
        break

    sets = input("How many sets? ")
    reps = input("How many reps per set? ")

    entry = f"{exercise} - {sets} sets of {reps} reps"
    workouts.append(entry)

print("\n--- Workout Summary ---")
for workout in workouts:
    print(workout)
