import os
from datetime import datetime

def calculate_total_reps(log_file="workout_log.txt"):
    total = 0

    try:
        with open(log_file, "r") as f:
            for line in f:
                if ":" not in line:
                    continue
                try:
                    reps_part = line.split(":")[1]
                    reps = int(reps_part.strip().split()[0])
                    total += reps
                except:
                    continue
    except FileNotFoundError:
        return 0

    return total


def generate_report():
    name = input("Client Name: ").strip()
    week = input("Week Number: ").strip()
    weight = input("Current Weight: ").strip()
    focus = input("Focus for Next Week: ").strip()

    total_reps = calculate_total_reps()

    os.makedirs("reports", exist_ok=True)

    filename = f"reports/{name}_Week_{week}_Report.txt"

    with open(filename, "w") as f:
        f.write("==== CLIENT PROGRESS REPORT ====\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write(f"Client: {name}\n")
        f.write(f"Week: {week}\n")
        f.write(f"Weight: {weight}\n")
        f.write(f"Total Reps This Week: {total_reps}\n")
        f.write(f"Next Week Focus: {focus}\n")

    print(f"\n✅ Smart report generated: {filename}")

generate_report()