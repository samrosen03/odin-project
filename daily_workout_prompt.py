import random

exercises = [
    "20 Pushups", "30 Squats", "15 Burpees",
    "1 Minute Plank", "10 Pullups", "40 Jumping Jacks",
    "20 Lunges", "15 Situps", "Sprint 100m"
]

daily_pick = random.choice(exercises)
print("💥 Your Workout Prompt for Today:")
print(f"➡️ {daily_pick}")
