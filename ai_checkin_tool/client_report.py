import json
import os

DATA_FILE = "data/checkins.json"


def load_checkins():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def build_client_report():
    checkins = load_checkins()

    if not checkins:
        print("No check-ins found.")
        return

    latest = checkins[-1]

    print("\n📋 CLIENT REPORT\n")
    print(f"Client: {latest['client']}")
    print(f"Weight: {latest['weight']}")
    print(f"Energy: {latest['energy']}/10")
    print(f"Sleep: {latest['sleep']}/10")
    print(f"Nutrition: {latest['nutrition']}/10")
    print(f"Stress: {latest['stress']}/10")

    print("\n✅ STRENGTHS")
    if int(latest["energy"]) >= 7:
        print("- Energy is strong")
    if int(latest["nutrition"]) >= 7:
        print("- Nutrition is solid")
    if int(latest["sleep"]) >= 7:
        print("- Sleep is solid")

    print("\n⚠️ NEEDS ATTENTION")
    if int(latest["energy"]) <= 5:
        print("- Energy is low")
    if int(latest["sleep"]) <= 5:
        print("- Sleep needs work")
    if int(latest["stress"]) >= 7:
        print("- Stress is high")
    if int(latest["nutrition"]) <= 5:
        print("- Nutrition needs improvement")

    print("\n🎯 COACH RECOMMENDATION")
    if int(latest["sleep"]) <= 5 or int(latest["stress"]) >= 7:
        print("Focus on recovery this week.")
    elif int(latest["nutrition"]) <= 5:
        print("Focus on nutrition consistency this week.")
    else:
        print("Keep momentum going and stay consistent.")


if __name__ == "__main__":
    build_client_report()