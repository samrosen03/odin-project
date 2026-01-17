import shutil
from datetime import datetime

def backup_log(source="workout_log.txt"):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        destination = f"backup_workout_log_{timestamp}.txt"
        shutil.copy(source, destination)
        print(f"✅ Backup saved as: {destination}")
    except FileNotFoundError:
        print("❌ workout_log.txt not found.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

backup_log()
