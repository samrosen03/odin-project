# read_workout_log.py

print("\n📖 Your Workout History:")

try:
    with open("workout_log.txt", "r") as file:
        lines = file.readlines()

        if not lines:
            print("No workouts logged yet.")
        else:
            for line in lines:
                print(f"• {line.strip()}")

except FileNotFoundError:
    print("Workout log file not found.")
