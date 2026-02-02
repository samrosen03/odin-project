def search_notes(log_file="workout_log.txt"):
    keyword = input("🔍 Enter keyword to search in notes: ").strip().lower()
    found = False

    try:
        with open(log_file, "r") as file:
            for line in file:
                if "| Note:" in line and keyword in line.lower():
                    print(f"📌 {line.strip()}")
                    found = True
        if not found:
            print("❌ No matching notes found.")
    except FileNotFoundError:
        print("⚠️ workout_log.txt not found.")

search_notes()
