def edit_entry(log_file="workout_log.txt"):
    target_date = input("Enter date to edit (YYYY-MM-DD): ").strip()

    try:
        with open(log_file, "r") as f:
            lines = f.readlines()

        updated_lines = []
        found = False

        for line in lines:
            if line.startswith(target_date):
                print(f"\nFound entry:\n{line.strip()}")
                new_data = input("Enter new workout data (e.g. Pushups: 50): ").strip()
                updated_lines.append(f"{target_date} - {new_data}\n")
                found = True
            else:
                updated_lines.append(line)

        if not found:
            print("No entry found for that date.")
            return

        with open(log_file, "w") as f:
            f.writelines(updated_lines)

        print("✅ Entry updated successfully.")

    except FileNotFoundError:
        print("⚠️ workout_log.txt not found.")


edit_entry()
