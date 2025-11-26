# total_reps_by_exercise.py

exercise_to_search = input("Which exercise do you want total reps for? ").lower()
total_reps = 0

try:
    with open("workout_log.txt", "r") as file:
        for line in file:
            if exercise_to_search in line.lower():
                try:
                    sets = int(line.split("did")[1].split("sets")[0].strip())
                    reps = int(line.split("sets of")[1].split("reps")[0].strip())
                    total_reps += sets * reps
                except:
                    continue

    print(f"\n💪 You’ve done a total of {total_reps} reps of {exercise_to_search.capitalize()}.")
except FileNotFoundError:
    print("No workout log found. Log something first!")
