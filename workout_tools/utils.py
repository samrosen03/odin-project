import json
from datetime import datetime

LOG_FILE = "data/workout_log.json"


def read_entries():
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Log file not found.")
        return []
    except json.JSONDecodeError:
        print("Log file is empty or invalid.")
        return []


def parse_entries():
    raw_entries = read_entries()
    parsed = []

    for entry in raw_entries:
        try:
            parsed.append({
                "date": datetime.strptime(entry["date"], "%Y-%m-%d"),
                "client": entry.get("client", "Unknown"),  # 👈 NEW
                "exercise": entry["exercise"],
                "reps": int(entry["reps"])
            })
        except (KeyError, ValueError, TypeError):
            continue

    return parsed