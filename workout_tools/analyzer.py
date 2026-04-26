import sys
import os
import json
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
    get_client_leaderboard,
)


def show_top_client_this_month():
    entries = get_entries_or_warn()
    if not entries:
        return

    today = datetime.now()
    month_entries = [
        e for e in entries
        if e["date"].year == today.year and e["date"].month == today.month
    ]

    if not month_entries:
        print("No workouts this month.")
        return

    totals = defaultdict(int)
    for e in month_entries:
        client = e.get("client", "Unknown")
        totals[client] += e["reps"]

    ranked = sorted(totals.items(), key=lambda x: x[1], reverse=True)

    print("\n🏆 TOP CLIENT THIS MONTH\n")
    for i, (client, reps) in enumerate(ranked, start=1):
        print(f"{i}. {client} → {reps} reps")

def show_recent_workouts(limit=5):
    entries = get_entries_or_warn()
    if not entries:
        return

    recent = sorted(entries, key=lambda e: e["date"], reverse=True)[:limit]

    print(f"\n🕒 LAST {len(recent)} WORKOUTS\n")
    for entry in recent:
        date = entry["date"].date()
        client = entry.get("client", "Unknown")
        exercise = entry["exercise"]
        reps = entry["reps"]
        print(f"{date} → {client} | {exercise} | {reps} reps")

def show_client_top_exercise(client_name):
    entries = get_entries_or_warn()
    if not entries:
        return

    client_entries = [
        e for e in entries
        if e.get("client", "").lower() == client_name.lower()
    ]

    if not client_entries:
        print(f"No data found for {client_name}")
        return

    totals = defaultdict(int)
    for e in client_entries:
        totals[e["exercise"]] += e["reps"]

    top_ex = max(totals, key=totals.get)
    top_reps = totals[top_ex]

    print(f"\n🏆 TOP EXERCISE — {client_name}\n")
    print(f"{top_ex} → {top_reps} reps")

def compare_clients(client1, client2):
    entries = get_entries_or_warn()
    if not entries:
        return

    def get_stats(name):
        client_entries = [
            e for e in entries
            if e.get("client", "").lower() == name.lower()
        ]

        if not client_entries:
            return None

        total_reps = sum(e["reps"] for e in client_entries)
        days = len({e["date"].date() for e in client_entries})

        totals = defaultdict(int)
        for e in client_entries:
            totals[e["exercise"]] += e["reps"]

        top_ex = max(totals, key=totals.get) if totals else "None"

        return total_reps, days, top_ex

    stats1 = get_stats(client1)
    stats2 = get_stats(client2)

    if not stats1 or not stats2:
        print("One or both clients not found.")
        return

    print(f"\n⚔️ CLIENT COMPARISON\n")
    print(f"{client1} vs {client2}\n")

    print(f"Total Reps: {stats1[0]} vs {stats2[0]}")
    print(f"Workout Days: {stats1[1]} vs {stats2[1]}")
    print(f"Top Exercise: {stats1[2]} vs {stats2[2]}")

def show_client_count():
    entries = get_entries_or_warn()
    if not entries:
        return

    clients = {e.get("client", "Unknown") for e in entries}

    print("\n👥 CLIENT COUNT\n")
    print(f"Total Unique Clients: {len(clients)}")

def show_summary():
    entries = get_entries_or_warn()
    if not entries:
        return

    total_reps = sum(e["reps"] for e in entries)
    workout_days = len({e["date"].date() for e in entries})
    streak = get_longest_streak()

    counts = defaultdict(int)
    for e in entries:
        counts[e["exercise"]] += 1

    top_exercise = max(counts, key=counts.get) if counts else "None"

    print("\n📋 WORKOUT SUMMARY\n")
    print(f"Total Reps: {total_reps}")
    print(f"Workout Days: {workout_days}")
    print(f"Most Logged Exercise: {top_exercise}")
    print(f"Longest Streak: {streak} days")


def show_best_day():
    entries = get_entries_or_warn()
    if not entries:
        return

    daily = defaultdict(int)

    for e in entries:
        day = e["date"].date()
        daily[day] += e["reps"]

    if not daily:
        print("No data available.")
        return

    best_day = max(daily, key=daily.get)
    best_reps = daily[best_day]

    print("\n🔥 BEST WORKOUT DAY\n")
    print(f"{best_day} → {best_reps} reps")


def show_high_value_clients():
    entries = get_entries_or_warn()
    if not entries:
        return

    totals = defaultdict(int)
    sessions = defaultdict(int)

    for e in entries:
        client = e.get("client", "Unknown")
        totals[client] += e["reps"]
        sessions[client] += 1

    ranked = sorted(totals.items(), key=lambda x: x[1], reverse=True)

    print("\n💰 HIGH VALUE CLIENTS (PRIORITIZE THESE)\n")
    for i, (client, reps) in enumerate(ranked[:5], start=1):
        print(f"{i}. {client} → {reps} reps | {sessions[client]} sessions")

def show_client_streak(client_name):
    entries = get_entries_or_warn()
    if not entries:
        return

    client_entries = [
        e for e in entries
        if e.get("client", "").lower() == client_name.lower()
    ]

    if not client_entries:
        print(f"No data found for {client_name}")
        return

    # Get unique workout days sorted
    days = sorted({e["date"].date() for e in client_entries})

    streak = 1
    longest = 1

    for i in range(1, len(days)):
        if (days[i] - days[i - 1]).days == 1:
            streak += 1
            longest = max(longest, streak)
        else:
            streak = 1

    print(f"\n🔥 STREAK — {client_name}\n")
    print(f"Current/Recent Streak: {streak} days")
    print(f"Longest Streak: {longest} days")

def show_client_revenue(rate_per_session=75):
    entries = get_entries_or_warn()
    if not entries:
        return

    sessions = defaultdict(int)

    for e in entries:
        client = e.get("client", "Unknown")
        sessions[client] += 1

    print("\n💵 CLIENT REVENUE\n")
    for client, count in sorted(sessions.items(), key=lambda x: x[1], reverse=True):
        revenue = count * rate_per_session
        print(f"{client} → ${revenue} ({count} sessions)")


def show_priority_clients():
    entries = get_entries_or_warn()
    if not entries:
        return

    totals = defaultdict(int)
    last_seen = {}

    for e in entries:
        client = e.get("client", "Unknown")
        totals[client] += e["reps"]

        if client not in last_seen or e["date"] > last_seen[client]:
            last_seen[client] = e["date"]

    today = datetime.now()

    scored = []
    for client in totals:
        days_off = (today - last_seen[client]).days
        score = totals[client] - (days_off * 50)
        scored.append((client, score, days_off, totals[client]))

    ranked = sorted(scored, key=lambda x: x[1], reverse=True)

    print("\n🎯 TOP 3 CLIENTS TO FOCUS TODAY\n")

    for i, (client, score, days_off, reps) in enumerate(ranked[:3], start=1):
        print(f"{i}. {client}")
        print(f"   Reps: {reps}")
        print(f"   Days inactive: {days_off}")
        print(f"   Priority score: {score}\n")


def save_last_command(command_string):
    os.makedirs("data", exist_ok=True)
    with open("data/last_command.txt", "w") as f:
        f.write(command_string)


def ensure_datetime(entry):
    if isinstance(entry["date"], str):
        entry["date"] = datetime.fromisoformat(entry["date"])
    return entry


def get_entries_or_warn():
    entries = parse_entries()

    if not entries:
        print("No workout data available.")
        return None

    return [ensure_datetime(e) for e in entries]


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


def show_top_exercises(limit=3):
    results = get_top_exercises(limit)

    if not results:
        print("No data available.")
        return

    print(f"\n🏆 Top {limit} Exercises\n")
    for name, reps in results:
        print(f"{name} → {reps} reps")


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
        f.write("date,client,exercise,reps\n")

        for e in entries:
            date = e["date"].date()
            client = e.get("client", "Unknown")
            exercise = e["exercise"]
            reps = e["reps"]
            f.write(f"{date},{client},{exercise},{reps}\n")

    print("📊 CSV exported to reports/workouts.csv")


def run_last_command():
    try:
        with open("data/last_command.txt", "r") as f:
            last = f.read().strip()

        if not last:
            print("No previous command found.")
            return

        print(f"\n🔁 Re-running last command: {last}\n")

        parts = last.split()
        if not parts:
            print("No previous command found.")
            return

        old_argv = sys.argv[:]
        try:
            sys.argv = [sys.argv[0]] + parts
            run_cli_mode(parts[0])
        finally:
            sys.argv = old_argv

    except FileNotFoundError:
        print("No previous command saved.")


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


def show_stats(exercise=None, client=None):
    entries = get_entries_or_warn()
    if not entries:
        return

    if client:
        entries = [e for e in entries if e.get("client", "").lower() == client.lower()]
        if not entries:
            print(f"No data found for client '{client}'")
            return

    if exercise:
        entries = [e for e in entries if e["exercise"].lower() == exercise.lower()]
        if not entries:
            print(f"No data found for exercise '{exercise}'")
            return

    total_reps = sum(e["reps"] for e in entries)
    unique_days = {e["date"].date() for e in entries}

    print("\n📊 WORKOUT STATS\n")

    if client:
        print(f"Client: {client}")

    if exercise:
        print(f"Exercise: {exercise}")

    print(f"Total Reps: {total_reps}")
    print(f"Workout Days: {len(unique_days)}")

    if not exercise and not client:
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

    filtered = [e for e in entries if start <= e["date"] <= end]

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

    filtered = [e for e in entries if start <= e["date"] <= end]

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


def list_clients():
    entries = get_entries_or_warn()
    if not entries:
        return

    clients = sorted({e["client"] for e in entries})

    print("\n👥 CLIENTS\n")
    for c in clients:
        print(f"- {c}")


def show_leaderboard():
    entries = get_entries_or_warn()
    if not entries:
        return

    ranked = get_client_leaderboard(entries)

    print("\n🏆 CLIENT LEADERBOARD\n")
    for i, (client, reps) in enumerate(ranked, start=1):
        print(f"{i}. {client} → {reps} reps")


def show_top_client_this_week():
    entries = get_entries_or_warn()
    if not entries:
        return

    today = datetime.now()
    week_ago = today - timedelta(days=7)

    weekly_entries = [e for e in entries if e["date"] >= week_ago]

    if not weekly_entries:
        print("No workouts this week.")
        return

    totals = defaultdict(int)
    for e in weekly_entries:
        client = e.get("client", "Unknown")
        totals[client] += e["reps"]

    ranked = sorted(totals.items(), key=lambda x: x[1], reverse=True)

    print("\n🏆 TOP CLIENT THIS WEEK\n")
    for i, (client, reps) in enumerate(ranked, start=1):
        print(f"{i}. {client} → {reps} reps")

def show_today_workouts():
    entries = get_entries_or_warn()
    if not entries:
        return

    today = datetime.now().date()
    today_entries = [e for e in entries if e["date"].date() == today]

    if not today_entries:
        print("\nNo workouts logged today.\n")
        return

    print("\n📅 TODAY’S WORKOUTS\n")
    for e in today_entries:
        client = e.get("client", "Unknown")
        exercise = e["exercise"]
        reps = e["reps"]
        print(f"{client} → {exercise} ({reps} reps)")

def show_at_risk_clients(days_threshold=3):
    entries = get_entries_or_warn()
    if not entries:
        return

    latest_by_client = {}
    for e in entries:
        client = e.get("client", "Unknown")
        date = e["date"]
        if client not in latest_by_client or date > latest_by_client[client]:
            latest_by_client[client] = date

    today = datetime.now()
    at_risk = []

    for client, last_date in latest_by_client.items():
        days_off = (today - last_date).days
        if days_off >= days_threshold:
            at_risk.append((client, days_off))

    if not at_risk:
        print("\n✅ No at-risk clients right now.\n")
        return

    print("\n⚠️ AT-RISK CLIENTS\n")
    for client, days in sorted(at_risk, key=lambda x: x[1], reverse=True):
        print(f"{client} → {days} days inactive")


def generate_at_risk_messages(days_threshold=3):
    entries = get_entries_or_warn()
    if not entries:
        return

    latest_by_client = {}
    for e in entries:
        client = e.get("client", "Unknown")
        date = e["date"]

        if client not in latest_by_client or date > latest_by_client[client]:
            latest_by_client[client] = date

    today = datetime.now()

    print("\n📩 REACH OUT LIST\n")

    found_any = False
    for client, last_date in latest_by_client.items():
        days_off = (today - last_date).days

        if days_off >= days_threshold:
            found_any = True

            if days_off >= 5:
                msg = f"Hey {client} — haven’t seen you in a bit. Let’s get back into it this week 💪"
            else:
                msg = f"Hey {client} — quick check-in. Let’s get a session in this week."

            print(f"{client}: {msg}")
            print(f"👉 COPY: {msg}\n")

    if not found_any:
        print("No at-risk clients to message.\n")


def check_client_inactivity(client_name, days_threshold=2):
    entries = get_entries_or_warn()
    if not entries:
        return

    client_entries = [
        e for e in entries
        if e.get("client", "").lower() == client_name.lower()
    ]

    if not client_entries:
        print(f"No data for {client_name}")
        return

    last_date = max(e["date"] for e in client_entries)
    today = datetime.now()

    days_off = (today - last_date).days

    if days_off >= days_threshold:
        print(f"\n⚠️ {client_name} hasn’t trained in {days_off} days")
    else:
        print(f"\n✅ {client_name} is on track ({days_off} day gap)")


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

def show_client_summary(client_name):
    entries = get_entries_or_warn()
    if not entries:
        return

    client_entries = [
        e for e in entries
        if e.get("client", "").lower() == client_name.lower()
    ]

    if not client_entries:
        print(f"No data found for {client_name}")
        return

    total_reps = sum(e["reps"] for e in client_entries)
    workout_days = len({e["date"].date() for e in client_entries})

    last_date = max(e["date"] for e in client_entries)
    days_inactive = (datetime.now() - last_date).days

    counts = defaultdict(int)
    for e in client_entries:
        counts[e["exercise"]] += e["reps"]

    top_exercise = max(counts, key=counts.get)

    print(f"\n📊 CLIENT SUMMARY — {client_name}\n")
    print(f"Total Reps: {total_reps}")
    print(f"Workout Days: {workout_days}")
    print(f"Top Exercise: {top_exercise}")
    print(f"Last Workout: {last_date.date()}")
    print(f"Days Inactive: {days_inactive}")

def daily_coach():
    print("\n🔥 DAILY COACH SYSTEM 🔥")
    print("\n1️⃣ AT-RISK CLIENTS (BOOK THESE)")
    generate_at_risk_messages()

    print("\n2️⃣ HIGH VALUE CLIENTS (KEEP THESE)")
    show_high_value_clients()

    print("\n3️⃣ ACTION PLAN")
    print("→ Send 3–5 reach-out texts")
    print("→ Check in with top 2 clients")
    print("→ Book at least 1 session today\n")


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


def generate_client_message():
    entries = get_entries_or_warn()
    if not entries:
        return

    total_reps = sum(e["reps"] for e in entries)
    days = {e["date"].date() for e in entries}
    streak = get_longest_streak()

    print("\n📩 CLIENT MESSAGE\n")

    if len(days) >= 4:
        print("You've been super consistent this week — keep it up. Proud of you.")
    elif streak >= 3:
        print("Nice streak going. Let’s keep that momentum rolling.")
    else:
        print("Let’s lock back in this week — small wins daily.")

    print(f"(Total reps logged: {total_reps})")


def generate_client_specific_message(client_name):
    entries = get_entries_or_warn()
    if not entries:
        return

    client_entries = [
        e for e in entries
        if e.get("client", "").lower() == client_name.lower()
    ]

    if not client_entries:
        print(f"No data found for {client_name}")
        return

    days = {e["date"].date() for e in client_entries}
    streak = get_longest_streak()

    print(f"\n📩 MESSAGE FOR {client_name}\n")

    if len(days) >= 4:
        msg = f"{client_name}, you’ve been super consistent lately — let’s keep building 💪"
    elif streak >= 3:
        msg = f"{client_name}, nice streak going — let’s keep that momentum rolling."
    else:
        msg = f"{client_name}, let’s lock back in this week. Small wins."

    print(msg)
    print(f"\n👉 COPY: {msg}")

def show_last_workout(client_name):
    entries = get_entries_or_warn()
    if not entries:
        return

    client_entries = [
        e for e in entries
        if e.get("client", "").lower() == client_name.lower()
    ]

    if not client_entries:
        print(f"No data found for {client_name}")
        return

    last_entry = max(client_entries, key=lambda e: e["date"])

    date = last_entry["date"].date()
    exercise = last_entry["exercise"]
    reps = last_entry["reps"]

    print(f"\n🕒 LAST WORKOUT — {client_name}\n")
    print(f"{date} → {exercise} ({reps} reps)")

def streak_warning():
    entries = get_entries_or_warn()
    if not entries:
        return

    last_date = max(e["date"] for e in entries)
    today = datetime.now()

    days_off = (today - last_date).days

    print("\n⚠️ STREAK CHECK\n")

    if days_off >= 3:
        print(f"You’ve missed {days_off} days. Time to get back in.")
    else:
        print("You’re staying consistent. Keep going.")


def show_exercise_rankings():
    entries = get_entries_or_warn()
    if not entries:
        return

    totals = defaultdict(int)
    for e in entries:
        totals[e["exercise"]] += e["reps"]

    ranked = sorted(totals.items(), key=lambda x: x[1], reverse=True)

    print("\n🏆 EXERCISE RANKINGS\n")
    for i, (ex, reps) in enumerate(ranked, start=1):
        print(f"{i}. {ex} → {reps} reps")


def clear_workouts():
    confirm = input("⚠️ This will delete all workout entries. Type 'yes' to confirm: ")

    if confirm.lower() != "yes":
        print("Cancelled.")
        return

    log_path = os.path.join("data", "workout_log.json")
    with open(log_path, "w") as f:
        json.dump([], f, indent=2)

    print("🧹 Workout data cleared.")


def generate_client_report(client_name):
    entries = get_entries_or_warn()
    if not entries:
        return

    client_entries = [
        e for e in entries
        if e.get("client", "").lower() == client_name.lower()
    ]

    if not client_entries:
        print(f"No data found for {client_name}")
        return

    total_reps = sum(e["reps"] for e in client_entries)
    days = {e["date"].date() for e in client_entries}

    totals = defaultdict(int)
    for e in client_entries:
        totals[e["exercise"]] += e["reps"]

    top_ex = max(totals, key=totals.get)

    print(f"\n📊 CLIENT REPORT — {client_name}\n")
    print(f"Workout Days: {len(days)}")
    print(f"Total Reps: {total_reps}")
    print(f"Top Exercise: {top_ex}")

    print("\n💬 Message:")
    if len(days) >= 4:
        print("Great consistency this week. Let’s keep building momentum.")
    elif len(days) >= 2:
        print("Solid work. Let’s aim for one more session this week.")
    else:
        print("Let’s get back on track—small wins this week.")


def show_help():
    print("""
Workout Analyzer Commands

total                     → Total reps by exercise
daily                     → Reps grouped by day
most                      → Most logged exercise
prs                       → Personal records
score                     → Consistency score
streak                    → Longest workout streak
search                    → Search exercise history
top [limit]               → Top exercises, optionally set limit
high                      → High intensity workouts
dashboard                 → Quick summary
invalid                   → Show invalid entries
average                   → Average reps per exercise
report                    → Export workout report
report-client NAME        → Generate report for a specific client
monthly                   → Monthly rep totals
stats [exercise] [client] → Overall workout summary, optionally filtered
range                     → Analyze workouts between two dates
range-top                 → Top exercise in a date range
check [days]              → Check inactivity (default 2 days)
inactive CLIENT_NAME      → Check inactivity for a client
at-risk                   → Show clients inactive for 3+ days
reach-out                 → Generate messages for at-risk clients
weekly                    → Show weekly workout report
message                   → Generate a client check-in message
message-client NAME       → Generate a check-in message for a specific client
warn                      → Show streak warning
rank                      → Show exercise rankings
clients                   → List all clients
leaderboard               → Rank clients by total reps
top-client-week           → Top clients ranked by reps this week
priority                  → Show high value clients
priority-today            → Show top 3 clients to focus today
daily-coach               → Run full daily coach system
clear                     → Delete all workout entries
csv                       → Export workouts as CSV file
scorecard                 → Show workout score (0–100)
repeat                    → Repeat last command
help                      → Show this help menu
revenue                   → Show estimated revenue by client
top-client-month          → Show top client this month
best-day                  → Show best workout day
summary                   → Show workout summary
recent                    → Show most recent workouts
clients                   → Show client count
today                     → Show today's workouts
client-summary NAME       → Show full breakdown for a client
top-exercise NAME         → Show top exercise for a client
streak-client NAME        → Show workout streak for a client
compare NAME1 NAME2      → Compare two clients
last-workout NAME        → Show most recent workout for a client
""")


def menu():
    actions = {
        "1": lambda: total_reps_by_exercise(get_entries_or_warn()),
        "2": lambda: reps_by_day(get_entries_or_warn()),
        "3": lambda: most_logged_exercise(get_entries_or_warn()),
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
        "22": generate_client_message,
        "23": streak_warning,
        "24": show_exercise_rankings,
        "25": run_last_command,
        "26": list_clients,
        "27": show_leaderboard,
        "28": lambda: print("Use CLI: inactive CLIENT_NAME"),
        "29": show_top_client_this_week,
        "30": lambda: print("Use CLI: message-client CLIENT_NAME"),
        "31": lambda: print("Use CLI: report-client CLIENT_NAME"),
        "32": show_at_risk_clients,
        "33": generate_at_risk_messages,
        "34": show_high_value_clients,
        "35": daily_coach,
        "36": show_priority_clients,
        "37": show_client_revenue,
        "38": show_top_client_this_month,
        "39": show_best_day,
        "40": show_summary,
        "41": show_recent_workouts,
        "42": show_client_count,
        "43": show_today_workouts,
        "44": lambda: print("Use CLI: client-summary CLIENT_NAME"),
        "45": lambda: print("Use CLI: top-exercise CLIENT_NAME"),
        "46": lambda: print("Use CLI: streak-client CLIENT_NAME"),
        "47": lambda: print("Use CLI: compare CLIENT_NAME1 CLIENT_NAME2"),
        "48": lambda: print("Use CLI: last-workout CLIENT_NAME")

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
        print("22) Generate client message")
        print("23) Show streak warning")
        print("24) Show exercise rankings")
        print("25) Repeat last command")
        print("26) List clients")
        print("27) Show leaderboard")
        print("28) Client inactivity check (CLI only)")
        print("29) Show top client this week")
        print("30) Generate client message (CLI only)")
        print("31) Generate client report (CLI only)")
        print("32) Show at-risk clients")
        print("33) Generate reach-out messages")
        print("34) Show high value clients")
        print("35) Run daily coach system")
        print("36) Show top 3 clients to focus today")
        print("37) Show client revenue")
        print("38) Show top client this month")
        print("39) Show best workout day")
        print("40) Show workout summary")
        print("41) Show most recent workouts")
        print("42) Show client count")
        print("43) Show today's workouts")
        print("44) Show client summary (CLI only)")
        print("45) Show client top exercise (CLI only)")
        print("46) Show client workout streak (CLI only)")
        print("47) Compare two clients (CLI only)")
        print("48) Show last workout (CLI only)")

        choice = input("Choose: ").strip()

        if choice == "7":
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Invalid option.")


def run_cli_mode(command):
    if command != "repeat":
        save_last_command(" ".join(sys.argv[1:]))

    entries = get_entries_or_warn()
    if not entries and command != "repeat":
        return

    if command == "total":
        total_reps_by_exercise(entries)
    elif command == "daily":
        reps_by_day(entries)
    elif command == "top-client-week":
        show_top_client_this_week()
    elif command == "clients":
        list_clients()
    elif command == "leaderboard":
        show_leaderboard()
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
    elif command == "inactive":
        if len(sys.argv) < 3:
            print("Usage: inactive CLIENT_NAME")
            return
        check_client_inactivity(sys.argv[2])
    elif command == "message-client":
        if len(sys.argv) < 3:
            print("Usage: message-client CLIENT_NAME")
            return
        generate_client_specific_message(sys.argv[2])
    elif command == "report-client":
        if len(sys.argv) < 3:
            print("Usage: report-client CLIENT_NAME")
            return
        generate_client_report(sys.argv[2])
    elif command == "best-day":
        show_best_day()
    elif command == "top-client-month":
        show_top_client_this_month()
    elif command == "summary":
        show_summary()
    elif command == "at-risk":
        show_at_risk_clients()
    elif command == "reach-out":
        generate_at_risk_messages()
    elif command == "high":
        show_high_intensity()
    elif command == "dashboard":
        show_dashboard()
    elif command == "invalid":
        show_invalid_entries()
    elif command == "recent":
        show_recent_workouts()
    elif command == "average":
        show_average_reps()
    elif command == "report":
        export_report()
    elif command == "monthly":
        show_monthly_reps()
    elif command == "stats":
        exercise = None
        client = None
        if len(sys.argv) > 2:
            exercise = sys.argv[2]
        if len(sys.argv) > 3:
            client = sys.argv[3]
        show_stats(exercise, client)
    elif command == "weekly":
        show_weekly_report()
    elif command == "range":
        if len(sys.argv) < 4:
            print("Usage: range YYYY-MM-DD YYYY-MM-DD")
            return
        show_range_summary(sys.argv[2], sys.argv[3])
    elif command == "range-top":
        if len(sys.argv) < 4:
            print("Usage: range-top YYYY-MM-DD YYYY-MM-DD")
            return
        show_top_exercise_in_range(sys.argv[2], sys.argv[3])
    elif command == "revenue":
        show_client_revenue()
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
    elif command == "client-count":
        show_client_count()
    elif command == "scorecard":
        show_workout_score()
    elif command == "message":
        generate_client_message()
    elif command == "warn":
        streak_warning()
    elif command == "rank":
        show_exercise_rankings()
    elif command == "priority":
        show_high_value_clients()
    elif command == "priority-today":
        show_priority_clients()
    elif command == "daily-coach":
        daily_coach()
    elif command == "repeat":
        run_last_command()
    elif command == "today":
        show_today_workouts()
    elif command == "client-summary":
        if len(sys.argv) < 3:
            print("Usage: client-summary CLIENT_NAME")
            return
        show_client_summary(sys.argv[2])
    elif command == "top-exercise":
        if len(sys.argv) < 3:
            print("Usage: top-exercise CLIENT_NAME")
            return
        show_client_top_exercise(sys.argv[2])
    elif command == "streak-client":
        if len(sys.argv) < 3:
            print("Usage: streak-client CLIENT_NAME")
            return
        show_client_streak(sys.argv[2])
    elif command == "compare":
        if len(sys.argv) < 4:
            print("Usage: compare NAME1 NAME2")
            return
        compare_clients(sys.argv[2], sys.argv[3])
    elif command == "last-workout":
        if len(sys.argv) < 3:
            print("Usage: last-workout CLIENT_NAME")
            return
        show_last_workout(sys.argv[2])
    else:
        print("Unknown command. Try: help")


def main():
    if len(sys.argv) > 1:
        run_cli_mode(sys.argv[1])
    else:
        menu()


if __name__ == "__main__":
    main()