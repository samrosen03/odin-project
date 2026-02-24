import datetime

LOG_FILE = "data/workout_log.txt"

def read_lines():
    try:
        with open(LOG_FILE, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def parse_entries():
    lines = read_lines()
    entries = []

    for line in lines:
        if " - " not in line or ":" not in line:
            continue

        try:
            date_str, data = line.strip().split(" - ", 1)
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")

            name, reps_part = data.split(":", 1)
            reps = int(reps_part.strip().split()[0])

            entries.append({
                "date": date_obj,
                "exercise": name.strip(),
                "reps": reps
            })

        except:
            continue

    return entries