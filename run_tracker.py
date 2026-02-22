from datetime import datetime

def log_run(script_name, log_file="run_history.txt"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_file, "a") as f:
        f.write(f"{now} - Ran: {script_name}\n")

    print(f"📘 Logged run of {script_name}")

# 👇 Change this depending on what you ran
log_run("trend_warning.py")