import json
import os

DATA_FILE = "data/checkins.json"


def load_checkins():
    if not os.path.exists(DATA_FILE):
        print("No check-ins found yet.")
        return []

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def show_history():
    checkins = load_checkins()

    if not checkins:
        return

    print("\n📋 CHECK-IN HISTORY\n")

    for c in checkins:
        print(f"Date: {c['date'][:10]}")
        print(f"Client: {c['client']}")
        print(f"Weight: {c['weight']}")
        print(f"Energy: {c['energy']}/10")
        print(f"Sleep: {c['sleep']}/10")
        print(f"Nutrition: {c['nutrition']}/10")
        print(f"Stress: {c['stress']}/10")
        print(f"Win: {c['win']}")
        print(f"Struggle: {c['struggle']}")
        print("-" * 30)


if __name__ == "__main__":
    show_history()