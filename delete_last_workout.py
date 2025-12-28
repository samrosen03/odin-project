def delete_last_entry(log_file="workout_log.txt"):
    try:
        with open(log_file, "r") as file:
            lines = file.readlines()

        if not lines:
            print("Log is already empty.")
            return

        removed = lines.pop()
        with open(log_file, "w") as file:
            file.writelines(lines)

        print(f"✅ Removed last entry: {removed.strip()}")
    except FileNotFoundError:
        print("❌ Log file not found.")

delete_last_entry()
