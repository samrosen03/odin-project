from workout_tools.utils import parse_entries
from collections import defaultdict


def total_reps_by_exercise(entries):
    totals = defaultdict(int)

    for entry in entries:
        totals[entry["exercise"]] += entry["reps"]

    print("\n📊 Total Reps By Exercise:")
    for name, total in totals.items():
        print(f"{name}: {total}")


def reps_by_day(entries):
    daily = defaultdict(int)

    for entry in entries:
        day = entry["date"].date()
        daily[day] += entry["reps"]

    print("\n📅 Reps By Day:")
    for day, total in sorted(daily.items()):
        print(f"{day}: {total}")


def most_logged_exercise(entries):
    counts = defaultdict(int)

    for entry in entries:
        counts[entry["exercise"]] += 1

    if not counts:
        print("No workouts logged.")
        return

    top = max(counts, key=counts.get)
    print(f"\n🏆 Most Logged Exercise: {top} ({counts[top]} times)")


def menu():
    entries = parse_entries()

    while True:
        print("\n==== ANALYZER MENU ====")
        print("1) Total reps by exercise")
        print("2) Reps by day")
        print("3) Most logged exercise")
        print("4) Quit")

        choice = input("Choose: ").strip()

        if choice == "1":
            total_reps_by_exercise(entries)
        elif choice == "2":
            reps_by_day(entries)
        elif choice == "3":
            most_logged_exercise(entries)
        elif choice == "4":
            break
        else:
            print("Invalid option.")


menu()