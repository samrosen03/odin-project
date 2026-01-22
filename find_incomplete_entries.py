def find_incomplete_entries(log_file="workout_log.txt"):
    try:
        with open(log_file, "r") as file:
            lines = file.readlines()

        print("🔍 Incomplete Entries:\n")
        found = False

        for line in lines:
            if " - " not in line:
                continue
            date, data = line.strip().split(" - ", 1)
            for part in data.split(","):
                if ":" in part:
                    name, reps = part.strip().split(":")
                    if not reps.strip():
                        print(f"⚠️ {date} - {name.strip()} is missing reps")
                        found = True

        if not found:
            print("✅ No incomplete entries found.")

    except FileNotFoundError:
        print("❌ workout_log.txt not found.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

find_incomplete_entries()
