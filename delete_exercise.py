def delete_exercise(target, log_file="workout_log.txt"):
    target = target.strip().lower()
    updated_lines = []

    try:
        with open(log_file, "r") as file:
            for line in file:
                if " - " not in line:
                    updated_lines.append(line)
                    continue

                date, data = line.strip().split(" - ", 1)
                exercises = data.split(",")
                remaining = []

                for item in exercises:
                    parts = item.strip().split(":")
                    if len(parts) == 2:
                        name = parts[0].strip().lower()
                        if name != target:
                            remaining.append(item.strip())

                if remaining:
                    updated_lines.append(f"{date} - {', '.join(remaining)}\n")

        with open(log_file, "w") as file:
            file.writelines(updated_lines)

        print(f"🗑️ All '{target}' entries removed from your workout log.")

    except FileNotFoundError:
        print("❌ workout_log.txt not found.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

# 👇 Replace with any exercise you want to delete
delete_exercise("Burpees")
