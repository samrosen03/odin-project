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