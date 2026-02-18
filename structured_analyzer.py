def read_log(file_path):
    try:
        with open(file_path, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        return []


def parse_entries(lines):
    parsed = []
    for line in lines:
        if " - " not in line:
            continue
        date, data = line.strip().split(" - ", 1)

        if ":" not in data:
            continue

        name, reps_str = data.split(":", 1)

        try:
            reps = int(reps_str.strip().split()[0])
        except:
            continue

        parsed.append({
            "date": date,
            "exercise": name.strip(),
            "reps": reps
        })

    return parsed


def calculate_totals(entries):
    totals = {}
    for entry in entries:
        name = entry["exercise"]
        reps = entry["reps"]

        if name not in totals:
            totals[name] = 0

        totals[name] += reps

    return totals


def display_results(totals):
    print("📊 Total Reps By Exercise:\n")
    for name, total in totals.items():
        print(f"{name}: {total}")


def main():
    lines = read_log("workout_log.txt")
    entries = parse_entries(lines)
    totals = calculate_totals(entries)
    display_results(totals)


main()
