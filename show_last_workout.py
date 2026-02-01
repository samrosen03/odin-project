def show_last_entry(log_file="workout_log.txt"):
    try:
        with open(log_file, "r") as file:
            lines = file.readlines()
            if lines:
                print("🕓 Last Logged Workout:")
                print(lines[-1].strip())
            else:
                print("⚠️ Log file is empty.")
    except FileNotFoundError:
        print("❌ workout_log.txt not found.")

show_last_entry()
