from datetime import datetime

print("\nWelcome to the Workout Logger!")

name = input("What's your name? ")
exercise = input("What exercise did you do today? ")
sets = input("How many sets? ")
reps = input("How many reps per set? ")

# Get today's date
today = datetime.now().strftime("%Y-%m-%d")

entry = f"{today} - {name} did {sets} sets of {reps} reps of {exercise}\n"

# Save it to a file
with open("workout_log.txt", "a") as file:
    file.write(entry)

print("\n✅ Workout saved with date!")
