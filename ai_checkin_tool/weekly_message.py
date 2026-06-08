import json
import os

DATA_FILE = "data/checkins.json"


def load_checkins():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def generate_weekly_message():
    checkins = load_checkins()

    if not checkins:
        print("No check-ins found.")
        return

    latest = checkins[-1]

    print("\n📩 WEEKLY CLIENT MESSAGE\n")

    print(f"Hey {latest['client']},\n")

    if int(latest["nutrition"]) >= 7:
        print("Great job staying consistent with your nutrition this week.")

    if int(latest["energy"]) >= 7:
        print("Your energy levels look strong.")

    if int(latest["sleep"]) <= 5:
        print("Focus on improving sleep and recovery this week.")

    if int(latest["stress"]) >= 7:
        print("Stress appears elevated, so make recovery a priority.")

    print("\nKeep up the good work!")
    print("\n- Coach Sam")


if __name__ == "__main__":
    generate_weekly_message()