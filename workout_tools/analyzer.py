import sys
from collections import defaultdict

from workout_tools.utils import parse_entries
from workout_tools.service import (
    get_personal_records,
    get_consistency_score,
    get_longest_streak,
    search_exercise,
    get_top_exercises,
)


def show_top_exercises():
    results = get_top_exercises()

    if not results:
        print("No data available.")
        return

    print("\n🏆 Top 3 Exercises\n")
    for name, reps in results:
        print(f"{name} → {reps} reps")


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


def show_personal_records():
    records = get_personal_records()
    if not records:
        print("No PR data yet.")
        return

    print("\n🏆 Personal Records:")
    for ex, reps in records.items():
        print(f"{ex} → {reps} reps")


def show_consistency_score():
    score = get_consistency_score()
    print(f"\n🔥 Consistency Score: {score} workout days logged")


def show_longest_streak():
    streak = get_longest_streak()
    print(f"\n🏅 Longest Streak: {streak} days")


def search_exercise_history():
    name = input("Search exercise: ").strip()
    results = search_exercise(name)

    if not results:
        print("No entries found.")
        return

    print(f"\n📜 History for {name}\n")
    for entry in results:
        date = entry["date"].date()
        reps = entry["reps"]
        print(f"{date} → {reps} reps")


def menu():
    entries = parse_entries()

    actions = {
        "1": lambda: total_reps_by_exercise(entries),
        "2": lambda: reps_by_day(entries),
        "3": lambda: most_logged_exercise(entries),
        "4": show_personal_records,
        "5": show_consistency_score,
        "6": show_longest_streak,
        "8": search_exercise_history,
        "9": show_top_exercises,
    }

    while True:
        print("\n==== ANALYZER MENU ====")
        print("1) Total reps by exercise")
        print("2) Reps by day")
        print("3) Most logged exercise")
        print("4) Show personal records")
        print("5) Show consistency score")
        print("6) Show longest streak")
        print("7) Quit")
        print("8) Search exercise history")
        print("9) Show top exercises")

        choice = input("Choose: ").strip()

        if choice == "7":
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Invalid option.")


def run_cli_mode(command):
    entries = parse_entries()

    if command == "total":
        total_reps_by_exercise(entries)
    elif command == "daily":
        reps_by_day(entries)
    elif command == "most":
        most_logged_exercise(entries)
    elif command == "prs":
        show_personal_records()
    elif command == "score":
        show_consistency_score()
    elif command == "streak":
        show_longest_streak()
    elif command == "search":
        search_exercise_history()
    elif command == "top":
        show_top_exercises()
    else:
        print("Unknown command. Try: total, daily, most, prs, score, streak, search, top")


def main():
    if len(sys.argv) > 1:
        run_cli_mode(sys.argv[1])
    else:
        menu()


if __name__ == "__main__":
    main()