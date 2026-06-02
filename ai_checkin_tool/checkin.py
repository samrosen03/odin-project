import json
import os
from datetime import datetime

DATA_FILE = "data/checkins.json"


def load_checkins():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_checkins(checkins):
    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w") as f:
        json.dump(checkins, f, indent=2)


def create_checkin():
    print("\nAI FITNESS CHECK-IN TOOL\n")

    client = input("Client name: ")
    weight = input("Weight: ")
    energy = input("Energy 1-10: ")
    sleep = input("Sleep 1-10: ")
    nutrition = input("Nutrition 1-10: ")
    stress = input("Stress 1-10: ")
    win = input("Biggest win this week: ")
    struggle = input("Biggest struggle this week: ")

    checkin = {
        "date": datetime.now().isoformat(),
        "client": client,
        "weight": weight,
        "energy": energy,
        "sleep": sleep,
        "nutrition": nutrition,
        "stress": stress,
        "win": win,
        "struggle": struggle,
    }

    checkins = load_checkins()
    checkins.append(checkin)
    save_checkins(checkins)

    print("\n✅ Check-in saved.")


if __name__ == "__main__":
    create_checkin()