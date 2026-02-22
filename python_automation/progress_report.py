import os
from datetime import datetime

def generate_report():
    name = input("Client Name: ").strip()
    week = input("Week Number: ").strip()
    weight = input("Current Weight: ").strip()
    pr = input("New PR (if any): ").strip()
    focus = input("Focus for Next Week: ").strip()

    os.makedirs("reports", exist_ok=True)

    filename = f"reports/{name}_Week_{week}_Report.txt"

    with open(filename, "w") as f:
        f.write("==== CLIENT PROGRESS REPORT ====\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write(f"Client: {name}\n")
        f.write(f"Week: {week}\n")
        f.write(f"Weight: {weight}\n")
        f.write(f"PR Achieved: {pr}\n")
        f.write(f"Next Week Focus: {focus}\n")

    print(f"\n✅ Report generated: {filename}")

generate_report()