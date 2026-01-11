def search_log(keyword, log_file="workout_log.txt"):
    keyword = keyword.strip().lower()
    found_lines = []

    try:
        with open(log_file, "r") as file:
            for line in file:
                if keyword in line.lower():
                    found_lines.append(line.strip())

        if found_lines:
            print(f"🔍 Found {len(found_lines)} result(s) for '{keyword}':\n")
            for line in found_lines:
                print(f"• {line}")
        else:
            print(f"❌ No results found for '{keyword}'.")

    except FileNotFoundError:
        print("❌ workout_log.txt not found.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

# 👇 Replace this with your own search term
search_log("pullups")
