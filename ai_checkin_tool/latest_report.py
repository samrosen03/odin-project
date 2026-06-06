import json
import os

DATA_FILE = "data/checkins.json"


def load_checkins():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def latest_report():
    checkins = load_checkins()

    if not checkins:
        print("No check-ins found.")
        return

    latest = checkins[-1]

    print("\n📋 LATEST CLIENT REPORT\n")

    print(f"Client: {latest['client']}")
    print(f"Weight: {latest['weight']}")
    print(f"Energy: {latest['energy']}/10")
    print(f"Sleep: {latest['sleep']}/10")
    print(f"Nutrition: {latest['nutrition']}/10")
    print(f"Stress: {latest['stress']}/10")
    print(f"Win: {latest['win']}")
    print(f"Struggle: {latest['struggle']}")


if __name__ == "__main__":
    latest_report()