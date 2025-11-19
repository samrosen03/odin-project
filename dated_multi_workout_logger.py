from datetime import datetime

print("\nWelcome to the Multi-Workout Logger!")

name = input("What's your name? ")
today = datetime.now().strftime("%Y-%m-%d")

entries = []

while True:
    exercise = input("\nEnter exercise name (or type 'done' to finish): ")
    if exercise.lower() == "done":
        break

    sets = input("How many sets? ")
    reps = input("How many reps per set? ")

    entry = f"{today} - {name} did {sets} sets of {reps} reps of {exercise}"
    entries.append(entry)

# Save all entries to the workout log file
with open("workout_log.txt", "a") as file:
    for e in entries:
        file.write(e + "\n")

print("\n✅ All workouts saved!")
