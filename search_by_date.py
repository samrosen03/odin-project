search_date = input("Enter date to search (YYYY-MM-DD): ")

found = False
with open("workout_log.txt", "r") as file:
    for line in file:
        if line.startswith(search_date):
            print("📅 Workout on", search_date)
            print(line.strip())
            found = True

if not found:
    print("❌ No workouts found for that date.")
