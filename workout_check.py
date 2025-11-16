# workout_check.py

goal_reps = 30
completed_reps = int(input("How many reps did you do today? "))

if completed_reps >= goal_reps:
    print("🔥 You hit your goal or more! Nice work.")
elif completed_reps >= goal_reps / 2:
    print("💪 Not bad — you got at least halfway there.")
else:
    print("😅 Let's push a little harder next time.")
