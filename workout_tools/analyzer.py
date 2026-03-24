import sys
import os
from collections import defaultdict
from datetime import datetime, timedelta

from workout_tools.utils import parse_entries
from workout_tools.service import (
    get_personal_records,
    get_consistency_score,
    get_longest_streak,
    search_exercise,
    get_top_exercises,
    get_high_intensity_workouts,
    get_invalid_entries,
    get_average_reps_per_exercise,
    generate_report,
    get_monthly_reps,
)


def get_entries_or_warn():
    entries = parse_entries()

    if not entries:
        print("No workout data available.")
        return None

    return entries


def show_top_exercises(limit=3):
    results = get_top_exercises(limit)

    if not results:
        print("No data available.")
        return

    print(f"\n🏆 Top {limit} Exercises\n")
    for name, reps in results:
        print(f"{name} → {reps} reps")


def total_reps_by_exercise(entries):
    if not entries:
        print("No workout data available.")
        return

    totals = defaultdict(int)
    for entry in entries:
        totals[entry["exercise"]] += entry["reps"]

    print("\n📊 Total Reps By Exercise:")
    for name, total in totals.items():
        print(f"{name}: {total}")


def reps_by_day(entries):
    if not entries:
        print("No workout data available.")
        return

    daily = defaultdict(int)
    for entry in entries:
        day = entry["date"].date()
        daily[day] += entry["reps"]

    print("\n📅 Reps By Day:")
    for day, total in sorted(daily.items()):
        print(f"{day}: {total}")


def most_logged_exercise(entries):
    if not entries:
        print("No workout data available.")
        return None

    counts = defaultdict(int)
    for entry in entries:
        counts[entry["exercise"]] += 1

    if not counts:
        print("No workouts logged.")
        return None

    top = max(counts, key=counts.get)
    print(f"\n🏆 Most Logged Exercise: {top} ({counts[top]} times)")
    return top


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


def show_invalid_entries():
    problems = get_invalid_entries()

    if not problems:
        print("No invalid entries found.")
        return

    print("\n⚠️ Invalid Entries\n")

    for entry, reason in problems:
        date = entry["date"].date()
        ex = entry["exercise"]
        reps = entry["reps"]
        print(f"{date} → {ex} ({reps}) — {reason}")


def show_average_reps():
    averages = get_average_reps_per_exercise()

    if not averages:
        print("No data available.")
        return

    print("\n📊 Average Reps Per Exercise\n")
    for ex, avg in averages.items():
        print(f"{ex} → {avg:.1f} avg reps")


def export_report():
    report = generate_report()

    os.makedirs("reports", exist_ok=True)

    with open("reports/workout_report.txt", "w") as f:
        f.write(report)

    print("📄 Report saved to reports/workout_report.txt")


def export_csv():
    entries = get_entries_or_warn()
    if not entries:
        return

    os.makedirs("reports", exist_ok=True)

    with open("reports/workouts.csv", "w") as f:
        f.write("date,exercise,reps\n")

        for e in entries:
            date = e["date"].date()
            exercise = e["exercise"]
            reps = e["reps"]
            f.write(f"{date},{exercise},{reps}\n")

    print("📊 CSV exported to reports/workouts.csv")


def show_high_intensity():
    results = get_high_intensity_workouts()

    if not results:
        print("No high intensity workouts found.")
        return

    print("\n🔥 High Intensity Workouts\n")

    for entry in results:
        date = entry["date"].date()
        ex = entry["exercise"]
        reps = entry["reps"]
        print(f"{date} → {ex} ({reps} reps)")


def show_dashboard():
    entries = get_entries_or_warn()
    if not entries:
        return

    total_reps = sum(e["reps"] for e in entries)
    consistency = get_consistency_score()
    streak = get_longest_streak()

    counts = defaultdict(int)
    for e in entries:
        counts[e["exercise"]] += 1

    most_ex = max(counts, key=counts.get) if counts else None

    print("\n📊 WORKOUT DASHBOARD\n")
    print(f"Total Reps Logged: {total_reps}")

    if most_ex:
        print(f"Most Logged Exercise: {most_ex}")

    print(f"Workout Days Logged: {consistency}")
    print(f"Longest Streak: {streak} days")


def show_monthly_reps():
    results = get_monthly_reps()

    if not results:
        print("No data available.")
        return

    print("\n📆 Total Reps By Month\n")
    for month, total in results.items():
        print(f"{month}: {total}")


def show_stats(exercise=None):
    entries = get_entries_or_warn()
    if not entries:
        return

    if exercise:
        entries = [e for e in entries if e["exercise"].lower() == exercise.lower()]

        if not entries:
            print(f"No data found for '{exercise}'")
            return

    total_reps = sum(e["reps"] for e in entries)
    unique_days = {e["date"].date() for e in entries}

    print("\n📊 WORKOUT STATS\n")

    if exercise:
        print(f"Exercise: {exercise}")

    print(f"Total Reps: {total_reps}")
    print(f"Workout Days: {len(unique_days)}")

    if not exercise:
        streak = get_longest_streak()
        print(f"Longest Streak: {streak} days")

        top = get_top_exercises()
        if top:
            print("\nTop Exercises:")
            for ex, reps in top:
                print(f"{ex} → {reps}")


def show_range_summary(start_str, end_str):
    try:
        start = datetime.strptime(start_str, "%Y-%m-%d")
        end = datetime.strptime(end_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD")
        return

    entries = get_entries_or_warn()
    if not entries:
        return

    filtered = [
        e for e in entries
        if start <= e["date"] <= end
    ]

    if not filtered:
        print("No data in this range.")
        return

    total_reps = sum(e["reps"] for e in filtered)
    unique_days = {e["date"].date() for e in filtered}

    print(f"\n📅 Workouts from {start_str} → {end_str}\n")
    print(f"Total Reps: {total_reps}")
    print(f"Workout Days: {len(unique_days)}")


def show_top_exercise_in_range(start_str, end_str):
    try:
        start = datetime.strptime(start_str, "%Y-%m-%d")
        end = datetime.strptime(end_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD")
        return

    entries = get_entries_or_warn()
    if not entries:
        return

    filtered = [
        e for e in entries
        if start <= e["date"] <= end
    ]

    if not filtered:
        print("No data in this range.")
        return

    totals = defaultdict(int)
    for e in filtered:
        totals[e["exercise"]] += e["reps"]

    top_ex = max(totals, key=totals.get)
    top_reps = totals[top_ex]

    print(f"\n🏆 Top Exercise from {start_str} → {end_str}\n")
    print(f"{top_ex}: {top_reps} reps")


def check_inactivity(days_threshold=2):
    entries = get_entries_or_warn()
    if not entries:
        return

    last_date = max(e["date"] for e in entries)
    today = datetime.now()

    days_inactive = (today - last_date).days

    if days_inactive >= days_threshold:
        print(f"\n⚠️ You haven’t worked out in {days_inactive} days")
        print("Time to get back on track.\n")
    else:
        print(f"\n✅ You’re on track! Last workout was {days_inactive} day(s) ago.\n")


def show_workout_score():
    entries = get_entries_or_warn()
    if not entries:
        return

    unique_days = {e["date"].date() for e in entries}
    consistency_score = min(len(unique_days), 30)

    total_reps = sum(e["reps"] for e in entries)
    reps_score = min(total_reps // 500, 40)

    streak = get_longest_streak()
    streak_score = min(streak * 2, 30)

    total_score = consistency_score + reps_score + streak_score

    print("\n🔥 WORKOUT SCORE\n")
    print(f"Score: {total_score}/100\n")
    print(f"Consistency: {len(unique_days)} days → {consistency_score} pts")
    print(f"Total Reps: {total_reps} → {reps_score} pts")
    print(f"Streak: {streak} days → {streak_score} pts")

    if total_score >= 80:
        print("\n🚀 Elite consistency. Keep going.")
    elif total_score >= 50:
        print("\n💪 Solid work. Stay consistent.")
    else:
        print("\n⚠️ Let’s step it up.")


def show_weekly_report():
    entries = get_entries_or_warn()
    if not entries:
        return

    today = datetime.now()
    week_ago = today - timedelta(days=7)

    weekly = [e for e in entries if e["date"] >= week_ago]

    if not weekly:
        print("No workouts this week.")
        return

    total_reps = sum(e["reps"] for e in weekly)
    days = {e["date"].date() for e in weekly}

    totals = defaultdict(int)
    for e in weekly:
        totals[e["exercise"]] += e["reps"]

    top_ex = max(totals, key=totals.get)

    print("\n📆 WEEKLY REPORT\n")
    print(f"Workout Days: {len(days)}")
    print(f"Total Reps: {total_reps}")
    print(f"Top Exercise: {top_ex}")

    if len(days) >= 4:
        print("\n💪 Great consistency this week.")
    else:
        print("\n⚠️ Let’s aim for more consistency next week.")


def clear_workouts():
    confirm = input("⚠️ This will delete all workout entries. Type 'yes' to confirm: ")

    if confirm.lower() != "yes":
        print("Cancelled.")
        return

    workouts_path = os.path.join("data", "workouts.txt")
    with open(workouts_path, "w") as f:
        f.write("")

    print("🧹 Workout data cleared.")


def show_help():
    print("""
Workout Analyzer Commands

total            → Total reps by exercise
daily            → Reps grouped by day
most             → Most logged exercise
prs              → Personal records
score            → Consistency score
streak           → Longest workout streak
search           → Search exercise history
top [limit]      → Top exercises, optionally set limit
high             → High intensity workouts
dashboard        → Quick summary
invalid          → Show invalid entries
average          → Average reps per exercise
report           → Export workout report
monthly          → Monthly rep totals
stats [exercise] → Overall workout summary, optionally filtered by exercise
range            → Analyze workouts between two dates
range-top        → Top exercise in a date range
check [days]     → Check inactivity (default 2 days)
weekly           → Show weekly workout report
clear            → Delete all workout entries
csv              → Export workouts as CSV file
scorecard        → Show workout score (0–100)
help             → Show this help menu
""")


def menu():
    actions = {
        "1": lambda: total_reps_by_exercise(parse_entries()),
        "2": lambda: reps_by_day(parse_entries()),
        "3": lambda: most_logged_exercise(parse_entries()),
        "4": show_personal_records,
        "5": show_consistency_score,
        "6": show_longest_streak,
        "8": search_exercise_history,
        "9": show_top_exercises,
        "10": show_high_intensity,
        "11": show_dashboard,
        "12": show_invalid_entries,
        "13": show_average_reps,
        "14": export_report,
        "15": show_monthly_reps,
        "16": show_stats,
        "17": clear_workouts,
        "18": export_csv,
        "19": check_inactivity,
        "20": show_workout_score,
        "21": show_weekly_report,
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
        print("10) Show high intensity workouts")
        print("11) Show dashboard summary")
        print("12) Show invalid entries")
        print("13) Show average reps per exercise")
        print("14) Export workout report")
        print("15) Show monthly reps")
        print("16) Show overall stats")
        print("17) Clear workout data")
        print("18) Export workouts as CSV")
        print("19) Check inactivity")
        print("20) Show workout score")
        print("21) Show weekly report")

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
        limit = 3

        if len(sys.argv) > 2:
            try:
                limit = int(sys.argv[2])
            except ValueError:
                print("Invalid number. Using default of 3.")

        show_top_exercises(limit)
    elif command == "high":
        show_high_intensity()
    elif command == "dashboard":
        show_dashboard()
    elif command == "invalid":
        show_invalid_entries()
    elif command == "average":
        show_average_reps()
    elif command == "report":
        export_report()
    elif command == "monthly":
        show_monthly_reps()
    elif command == "stats":
        exercise = sys.argv[2] if len(sys.argv) > 2 else None
        show_stats(exercise)
    elif command == "weekly":
        show_weekly_report()
    elif command == "range":
        if len(sys.argv) < 4:
            print("Usage: range YYYY-MM-DD YYYY-MM-DD")
            return

        start = sys.argv[2]
        end = sys.argv[3]
        show_range_summary(start, end)
    elif command == "range-top":
        if len(sys.argv) < 4:
            print("Usage: range-top YYYY-MM-DD YYYY-MM-DD")
            return

        start = sys.argv[2]
        end = sys.argv[3]
        show_top_exercise_in_range(start, end)
    elif command == "help":
        show_help()
    elif command == "clear":
        clear_workouts()
    elif command == "csv":
        export_csv()
    elif command == "check":
        threshold = 2

        if len(sys.argv) > 2:
            try:
                threshold = int(sys.argv[2])
            except ValueError:
                print("Invalid number. Using default of 2.")

        check_inactivity(threshold)
    elif command == "scorecard":
        show_workout_score()
    else:
        print("Unknown command. Try: help")


def main():
    if len(sys.argv) > 1:
        run_cli_mode(sys.argv[1])
    else:
        menu()


if __name__ == "__main__":
    main()