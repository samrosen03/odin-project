import time

def countdown_timer(seconds):
    while seconds > 0:
        print(f"{seconds} seconds remaining...")
        time.sleep(1)
        seconds -= 1
    print("⏰ Time's up! Move to the next exercise!")

# List of workout moves
exercises = ["Push-ups", "Squats", "Plank"]
duration = 10  # seconds per move

for move in exercises:
    print(f"\n⏱️ Get ready for: {move}")
    countdown_timer(duration)
