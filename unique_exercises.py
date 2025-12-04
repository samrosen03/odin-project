unique_exercises = set()

try:
    with open("workout_log.txt", "r") as file:
        for line in file:
            words = line.strip().split()
            for word in words:
                # crude filter: assume exercises are capitalized and alphabetic
                if word.isalpha() and word[0].isupper():
                    unique_exercises.add(word)

    print(f"🏋️‍♂️ Unique exercises logged: {len(unique_exercises)}")
    print("📋 Exercises:", ', '.join(sorted(unique_exercises)))

except FileNotFoundError:
    print("No workout log found.")
