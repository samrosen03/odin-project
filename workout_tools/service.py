from workout_tools.utils import parse_entries
from collections import defaultdict


def get_all_entries():
    return parse_entries()


def get_total_reps():
    entries = parse_entries()
    total = sum(e["reps"] for e in entries)
    return total


def get_total_reps_by_exercise():
    entries = parse_entries()
    totals = defaultdict(int)

    for e in entries:
        totals[e["exercise"]] += e["reps"]

    return dict(totals)


def get_most_logged_exercise():
    entries = parse_entries()
    counts = defaultdict(int)

    for e in entries:
        counts[e["exercise"]] += 1

    if not counts:
        return None

    return max(counts, key=counts.get)
def get_personal_records():
    from collections import defaultdict
    entries = parse_entries()
    
    records = defaultdict(int)

    for e in entries:
        if e["reps"] > records[e["exercise"]]:
            records[e["exercise"]] = e["reps"]

    return dict(records)
def get_consistency_score():
    entries = parse_entries()

    unique_days = set()

    for e in entries:
        unique_days.add(e["date"].date())

    return len(unique_days)
from datetime import timedelta

def get_longest_streak():
    entries = parse_entries()

    if not entries:
        return 0

    # Get unique workout days
    unique_days = sorted({e["date"].date() for e in entries})

    longest = 1
    current = 1

    for i in range(1, len(unique_days)):
        if unique_days[i] == unique_days[i - 1] + timedelta(days=1):
            current += 1
            longest = max(longest, current)
        else:
            current = 1

    return longest
def search_exercise(exercise_name):
    entries = parse_entries()

    results = []

    for entry in entries:
        if entry["exercise"].lower() == exercise_name.lower():
            results.append(entry)

    return results
def get_top_exercises(limit=3):
    entries = parse_entries()
    totals = defaultdict(int)

    for e in entries:
        totals[e["exercise"]] += e["reps"]

    sorted_exercises = sorted(
        totals.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return sorted_exercises[:limit]
def get_high_intensity_workouts(threshold=50):
    entries = parse_entries()

    results = []

    for e in entries:
        if e["reps"] >= threshold:
            results.append(e)

    return results
def get_invalid_entries():
    entries = parse_entries()
    problems = []

    for e in entries:

        if not e["exercise"]:
            problems.append((e, "Missing exercise name"))

        elif e["reps"] <= 0:
            problems.append((e, "Invalid rep count"))

    return problems
    
def get_average_reps_per_exercise():
    entries = parse_entries()

    totals = defaultdict(int)
    counts = defaultdict(int)

    for e in entries:
        exercise = e["exercise"]
        totals[exercise] += e["reps"]
        counts[exercise] += 1

    averages = {}

    for exercise in totals:
        averages[exercise] = totals[exercise] / counts[exercise]

    return averages
def generate_report():
    entries = parse_entries()

    if not entries:
        return "No workout data."

    total_reps = sum(e["reps"] for e in entries)

    unique_days = {e["date"].date() for e in entries}

    totals = defaultdict(int)
    for e in entries:
        totals[e["exercise"]] += e["reps"]

    top = sorted(totals.items(), key=lambda x: x[1], reverse=True)[:3]

    report = []
    report.append("WORKOUT SUMMARY\n")
    report.append(f"Total Reps: {total_reps}")
    report.append(f"Workout Days: {len(unique_days)}")

    report.append("\nTop Exercises:")

    for ex, reps in top:
        report.append(f"{ex} - {reps}")

    return "\n".join(report)

def get_monthly_reps():
    entries = parse_entries()
    monthly_totals = defaultdict(int)

    for e in entries:
        month = e["date"].strftime("%Y-%m")
        monthly_totals[month] += e["reps"]

    return dict(sorted(monthly_totals.items()))