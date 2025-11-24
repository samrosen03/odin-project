# search_workouts.py

exercise_to_search = input("Enter an exercise to search for: ").lower()

found = False

try:
    with open("workout_log.txt", "r") as file:
        print(f"\n📄 Results for: {exercise_to_search}")
        for line in file:
            if exercise_to_search in line.lower():
                print(f"• {line.strip()}")
                found = True

    if not found:
        print("No matching workouts found.")

except FileNotFoundError:
    print("Workout log not found. Run a workout logger first.")
