# workout_logger.py

name = input("What's your name? ")
exercise = input("What exercise did you do today? ")
sets = input("How many sets? ")
reps = input("How many reps per set? ")

summary = f"{name} did {sets} sets of {reps} reps of {exercise}\n"

# Save it to a file
with open("workout_log.txt", "a") as file:
    file.write(summary)

print("\n✅ Workout saved to workout_log.txt!")
