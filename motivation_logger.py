from datetime import datetime

def log_motivation(log_file="motivation_log.txt"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    message = input("💭 What's your motivation today? ").strip()

    if message:
        with open(log_file, "a") as file:
            file.write(f"{now} - {message}\n")
        print("✅ Motivation saved!")
    else:
        print("⚠️ You didn't write anything!")

log_motivation()
