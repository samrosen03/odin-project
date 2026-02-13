from datetime import datetime

LOG_FILE = "workout_log.txt"

def log_workout():
    date = datetime.now().strftime("%Y-%m-%d")
    exercise = input("Exercise: ").strip()
    reps = input("Reps: ").strip()

    if exercise and reps:
        with open(LOG_FILE, "a") as f:
            f.write(f"{date} - {exercise}: {reps}\n")
        print("✅ Workout logged.\n")
    else:
        print("⚠️ Invalid input.\n")


def show_last():
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            if lines:
                print("\n🕓 Last Workout:")
                print(lines[-1])
            else:
                print("Log is empty.\n")
    except FileNotFoundError:
        print("No log file found.\n")


def main():
    while True:
        print("==== Workout App ====")
        print("1. Log Workout")
        print("2. Show Last Workout")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            log_workout()
        elif choice == "2":
            show_last()
        elif choice == "3":
            print("👋 Exiting app.")
            break
        else:
            print("Invalid choice.\n")


main()
