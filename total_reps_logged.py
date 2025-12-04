import re

total_reps = 0

try:
    with open("workout_log.txt", "r") as file:
        for line in file:
            numbers = re.findall(r'\b\d+\b', line)
            total_reps += sum(int(num) for num in numbers)

    print(f"💪 Total reps logged: {total_reps}")

except FileNotFoundError:
    print("Workout log file not found. Start logging to see results!")
