import json

def convert_to_json(txt_file="workout_log.txt", json_file="workout_log.json"):
    workouts = []

    try:
        with open(txt_file, "r") as file:
            for line in file:
                if " - " not in line:
                    continue

                date, data = line.strip().split(" - ", 1)

                if ":" not in data:
                    continue

                exercise, reps = data.split(":", 1)

                workouts.append({
                    "date": date,
                    "exercise": exercise.strip(),
                    "reps": reps.strip()
                })

        with open(json_file, "w") as outfile:
            json.dump(workouts, outfile, indent=4)

        print(f"✅ Converted log to {json_file}")

    except FileNotFoundError:
        print("⚠️ workout_log.txt not found.")

convert_to_json()
