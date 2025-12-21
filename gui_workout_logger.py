import tkinter as tk
from datetime import datetime

def log_workout():
    workout = entry.get()
    if workout.strip() == "":
        return
    with open("workout_log.txt", "a") as file:
        file.write(f"{datetime.now().date()} - {workout}\n")
    entry.delete(0, tk.END)

# GUI setup
root = tk.Tk()
root.title("Workout Logger")

tk.Label(root, text="Enter your workout:").pack()
entry = tk.Entry(root, width=40)
entry.pack()

tk.Button(root, text="Log Workout", command=log_workout).pack()

root.mainloop()
