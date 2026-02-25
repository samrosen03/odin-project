import datetime

LOG_FILE = "data/workout_log.txt"

def parse_entries():
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Log file not found.")
        return []

    entries = []
    skipped = 0

    for line in lines:
        if " - " not in line or ":" not in line:
            skipped += 1
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
            skipped += 1

    print(f"\nParsed {len(entries)} entries.")
    if skipped:
        print(f"Skipped {skipped} malformed lines.")

    return entries