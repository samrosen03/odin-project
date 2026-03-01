import os

def run(script_path):
    os.system(f"python3 {script_path}")

def menu():
    while True:
        print("\n==== ODIN PROJECT TOOLBOX ====")
        print("1) Log workout (workout_app)")
        print("2) Show last workout")
        print("3) Weekly summary")
        print("4) PR detector")
        print("5) Progress report generator")
        print("6) Quote fetcher (API practice)")
        print("7) Quit")

        choice = input("Choose: ").strip()

        if choice == "1":
            run("workout_tools/workout_app.py")
        elif choice == "2":
            run("workout_tools/show_last_workout.py")
        elif choice == "3":
            run("workout_tools/weekly_summary.py")
        elif choice == "4":
            run("workout_tools/pr_detector.py")
        elif choice == "5":
            run("python_automation/progress_report.py")
        elif choice == "6":
            run("api_integration/quote_fetcher.py")
        elif choice == "7":
            print("Later 👋")
            break
        else:
            print("Invalid choice.")

menu()