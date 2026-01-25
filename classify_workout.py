def classify_workout():
    try:
        reps = int(input("Enter total reps completed today: "))
        if reps < 50:
            level = "Light"
        elif reps <= 100:
            level = "Moderate"
        else:
            level = "Intense"
        print(f"🔥 Your workout intensity: {level}")
    except ValueError:
        print("⚠️ Please enter a valid number.")

classify_workout()
