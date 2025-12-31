def write_summary(log_file="workout_log.txt", output_file="summary_report.txt"):
    total_lines = 0
    exercises_logged = set()

    try:
        with open(log_file, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                total_lines += 1

                # Expecting: DATE - exercise:reps, exercise:reps
                if " - " not in line:
                    continue

                _, workout_data = line.split(" - ", 1)
                exercise_parts = workout_data.split(",")

                for ex in exercise_parts:
                    parts = ex.strip().split(":")
                    if len(parts) == 2:
                        name = parts[0].strip()
                        exercises_logged.add(name)

        with open(output_file, "w") as out:
            out.write(f"📄 Total workout entries: {total_lines}\n\n")
            out.write("🏋️ Exercises logged:\n")
            for exercise in sorted(exercises_logged):
                out.write(f"- {exercise}\n")

        print(f"✅ Summary written to {output_file}")

    except FileNotFoundError:
        print("❌ workout_log.txt not found.")

write_summary()

