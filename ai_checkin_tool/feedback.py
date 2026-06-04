def generate_feedback(checkin):
    print("\n🤖 AI COACH FEEDBACK\n")

    if int(checkin["sleep"]) <= 5:
        print("⚠️ Sleep is low. Focus on getting to bed earlier this week.")

    if int(checkin["energy"]) <= 5:
        print("⚠️ Energy is low. Prioritize recovery and hydration.")

    if int(checkin["stress"]) >= 8:
        print("⚠️ Stress is high. Consider walks, breathing work, or downtime.")

    if int(checkin["nutrition"]) >= 8:
        print("✅ Nutrition looks great. Keep that momentum going.")

    print(f"\n🏆 Biggest Win: {checkin['win']}")
    print(f"🎯 Main Focus: {checkin['struggle']}")


def compare_last_two_checkins(checkins):
    if len(checkins) < 2:
        print("\nNeed at least 2 check-ins to compare trends.")
        return

    current = checkins[-1]
    previous = checkins[-2]

    print("\n📈 CHECK-IN TRENDS\n")

    for field in ["energy", "sleep", "nutrition", "stress"]:
        change = int(current[field]) - int(previous[field])

        if change > 0:
            print(f"{field.title()}: +{change}")
        elif change < 0:
            print(f"{field.title()}: {change}")
        else:
            print(f"{field.title()}: No Change")