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