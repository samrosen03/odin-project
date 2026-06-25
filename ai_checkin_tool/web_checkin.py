import json
import os
from datetime import datetime

from flask import Flask, request

app = Flask(__name__)

DATA_FILE = "data/checkins.json"
COACH_PASSWORD = "coach123"


def load_checkins():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_checkins(checkins):
    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w") as f:
        json.dump(checkins, f, indent=2)


def is_coach_logged_in():
    return request.args.get("password") == COACH_PASSWORD


def coach_dashboard_link():
    return f"/dashboard?password={COACH_PASSWORD}"


def generate_coach_feedback(checkin):
    feedback = []

    energy = int(checkin["energy"])
    sleep = int(checkin["sleep"])
    nutrition = int(checkin["nutrition"])
    stress = int(checkin["stress"])

    if nutrition >= 7:
        feedback.append("Great job staying consistent with your nutrition this week.")

    if energy >= 7:
        feedback.append("Your energy looks solid, which is a good sign your routine is supporting you.")

    if sleep <= 5:
        feedback.append("Sleep looks like the biggest opportunity this week. Aim to improve your bedtime routine and recovery.")

    if stress >= 7:
        feedback.append("Stress is elevated, so focus on recovery, hydration, walks, and keeping training manageable.")

    if energy <= 5:
        feedback.append("Energy is low, so avoid trying to crush every workout. Focus on consistency and recovery.")

    if not feedback:
        feedback.append("Overall, this looks like a steady week. Keep building consistency and focus on one small improvement.")

    return feedback


def build_trend_html(current, previous):
    if not previous:
        return ""

    metrics = ["energy", "sleep", "nutrition", "stress"]
    trend_html = "<h4>📈 Progress Since Last Check-In</h4><ul>"

    for metric in metrics:
        diff = int(current[metric]) - int(previous[metric])

        if diff > 0:
            trend_html += f"<li>{metric.title()}: +{diff}</li>"
        elif diff < 0:
            trend_html += f"<li>{metric.title()}: {diff}</li>"
        else:
            trend_html += f"<li>{metric.title()}: No Change</li>"

    trend_html += "</ul>"
    return trend_html


def calculate_weight_change(client_checkins):
    if len(client_checkins) < 2:
        return "Weight Change: Need at least 2 check-ins"

    try:
        first_weight = float(client_checkins[0][1]["weight"])
        latest_weight = float(client_checkins[-1][1]["weight"])
    except ValueError:
        return "Weight Change: Invalid weight data"

    change = latest_weight - first_weight

    if change > 0:
        return f"⬆️ Weight Change: +{change:.1f} lbs"
    elif change < 0:
        return f"⬇️ Weight Change: {change:.1f} lbs"
    else:
        return "➡️ Weight Change: No Change"


def build_client_summary(client_checkins):
    total = len(client_checkins)

    avg_energy = round(sum(int(c[1]["energy"]) for c in client_checkins) / total, 1)
    avg_sleep = round(sum(int(c[1]["sleep"]) for c in client_checkins) / total, 1)
    avg_nutrition = round(sum(int(c[1]["nutrition"]) for c in client_checkins) / total, 1)
    avg_stress = round(sum(int(c[1]["stress"]) for c in client_checkins) / total, 1)

    latest = client_checkins[-1][1]

    return f"""
    <h2>📊 Client Summary</h2>

    <p><strong>Total Check-Ins:</strong> {total}</p>
    <p><strong>Average Energy:</strong> {avg_energy}/10</p>
    <p><strong>Average Sleep:</strong> {avg_sleep}/10</p>
    <p><strong>Average Nutrition:</strong> {avg_nutrition}/10</p>
    <p><strong>Average Stress:</strong> {avg_stress}/10</p>

    <p><strong>Latest Win:</strong> {latest['win']}</p>
    <p><strong>Latest Struggle:</strong> {latest['struggle']}</p>

    <hr>
    """


@app.route("/")
def home():
    return """
    <h1>AI Check-In Tool is running ✅</h1>
    <p>Go to <a href="/checkin">/checkin</a> to submit a check-in.</p>
    <p>Go to <a href="/dashboard">/dashboard</a> to view coach dashboard.</p>
    """


@app.route("/checkin", methods=["GET", "POST"])
def checkin():
    if request.method == "POST":
        checkin_data = {
            "date": datetime.now().isoformat(),
            "client": request.form.get("client"),
            "weight": request.form.get("weight"),
            "energy": request.form.get("energy"),
            "sleep": request.form.get("sleep"),
            "nutrition": request.form.get("nutrition"),
            "stress": request.form.get("stress"),
            "win": request.form.get("win"),
            "struggle": request.form.get("struggle"),
            "goal": request.form.get("goal"),
            "coach_note": "",
        }

        checkins = load_checkins()
        checkins.append(checkin_data)
        save_checkins(checkins)

        feedback = generate_coach_feedback(checkin_data)
        feedback_html = "".join(f"<li>{item}</li>" for item in feedback)

        return f"""
        <h1>Check-in Submitted ✅</h1>

        <p><strong>Client:</strong> {checkin_data['client']}</p>
        <p><strong>Weight:</strong> {checkin_data['weight']}</p>
        <p><strong>Goal:</strong> {checkin_data['goal']}</p>
        <p><strong>Energy:</strong> {checkin_data['energy']}/10</p>
        <p><strong>Sleep:</strong> {checkin_data['sleep']}/10</p>
        <p><strong>Nutrition:</strong> {checkin_data['nutrition']}/10</p>
        <p><strong>Stress:</strong> {checkin_data['stress']}/10</p>
        <p><strong>Win:</strong> {checkin_data['win']}</p>
        <p><strong>Struggle:</strong> {checkin_data['struggle']}</p>

        <hr>

        <h2>🤖 Coach Feedback</h2>
        <ul>{feedback_html}</ul>

        <p><strong>Main Focus:</strong> {checkin_data['struggle']}</p>

        <br>
        <a href="/checkin">Submit another check-in</a><br>
        <a href="{coach_dashboard_link()}">View dashboard</a>
        """

    return """
    <h1>AI Fitness Check-In</h1>

    <form method="POST">
        <label>Client Name:</label><br>
        <input name="client" required><br><br>

        <label>Weight:</label><br>
        <input name="weight" required><br><br>

        <label>Energy 1-10:</label><br>
        <input name="energy" type="number" min="1" max="10" required><br><br>

        <label>Sleep 1-10:</label><br>
        <input name="sleep" type="number" min="1" max="10" required><br><br>

        <label>Nutrition 1-10:</label><br>
        <input name="nutrition" type="number" min="1" max="10" required><br><br>

        <label>Stress 1-10:</label><br>
        <input name="stress" type="number" min="1" max="10" required><br><br>
<label>Primary Goal:</label><br>

<select name="goal" required>
    <option value="">Select Goal</option>
    <option>Lose Fat</option>
    <option>Build Muscle</option>
    <option>Improve Strength</option>
    <option>Improve Endurance</option>
    <option>General Health</option>
</select>

<br><br>

        <label>Biggest win this week:</label><br>
        <textarea name="win" required></textarea><br><br>

        <label>Biggest struggle this week:</label><br>
        <textarea name="struggle" required></textarea><br><br>

        <button type="submit">Submit Check-In</button>
    </form>
    """


@app.route("/dashboard")
def dashboard():
    if not is_coach_logged_in():
        return """
        <h1>Coach Login</h1>
        <form method="GET" action="/dashboard">
            <input name="password" type="password" placeholder="Coach password">
            <button type="submit">Login</button>
        </form>
        """

    checkins = load_checkins()
    cards = ""

    if not checkins:
        return f"""
        <h1>Coach Dashboard</h1>

        <p>No check-ins yet.</p>

        <p><a href="/checkin">Submit new check-in</a></p>

        <p>
            <a href="/search?password={COACH_PASSWORD}">
                Search Clients
            </a>
        </p>
        """

    for checkin_id, c in reversed(list(enumerate(checkins))):
        status = "✅"

        checkin_date = datetime.fromisoformat(c["date"])
        days_since = (datetime.now() - checkin_date).days

        followup = ""
        if days_since >= 7:
            followup = " 🚨 Follow Up"

        if (
            int(c["sleep"]) <= 4
            or int(c["stress"]) >= 8
            or int(c["energy"]) <= 4
        ):
            status = "🚨 Needs Attention"

        cards += f"""
        <div style="border:1px solid #ccc; padding:15px; margin:15px 0;">
            <h2>
                <a href="/client/{c['client']}?password={COACH_PASSWORD}">
                    {c['client']}
                </a>
            </h2>

            <p><strong>Status:</strong> {status}</p>
            <p><strong>Last Check-In:</strong> {days_since} day(s) ago{followup}</p>
            <p><strong>Date:</strong> {c['date'][:10]}</p>
            <p><strong>Weight:</strong> {c['weight']}</p>
            <p><strong>Energy:</strong> {c['energy']}/10</p>
            <p><strong>Sleep:</strong> {c['sleep']}/10</p>
            <p><strong>Nutrition:</strong> {c['nutrition']}/10</p>
            <p><strong>Stress:</strong> {c['stress']}/10</p>
            <p><strong>Win:</strong> {c['win']}</p>
            <p><strong>Struggle:</strong> {c['struggle']}</p>

            <p><strong>Coach Note:</strong> {c.get('coach_note', 'None yet')}</p>

            <form method="POST" action="/note/{checkin_id}?password={COACH_PASSWORD}">
                <input name="note" placeholder="Add coach note">
                <button type="submit">Save Note</button>
            </form>
        </div>
        """

    return f"""
    <h1>Coach Dashboard</h1>

    <p><a href="/checkin">Submit new check-in</a></p>

    <p>
        <a href="/search?password={COACH_PASSWORD}">
            Search Clients
        </a>
    </p>

    {cards}
    """


@app.route("/client/<client_name>")
def client_history(client_name):
    if not is_coach_logged_in():
        return """
        <h1>Coach Login</h1>
        <form method="GET">
            <input name="password" type="password" placeholder="Coach password">
            <button type="submit">Login</button>
        </form>
        """

    checkins = load_checkins()

    client_checkins = [
        (checkin_id, c)
        for checkin_id, c in enumerate(checkins)
        if c["client"].lower() == client_name.lower()
    ]

    if not client_checkins:
        return f"<h1>No check-ins found for {client_name}</h1>"

    weight_change = calculate_weight_change(client_checkins)
    summary_html = build_client_summary(client_checkins)

    history = ""
    previous = None

    for checkin_id, c in reversed(client_checkins):
        trend_html = build_trend_html(c, previous)

        history += f"""
        <div style="border:1px solid #ccc; padding:15px; margin:15px 0;">
            <p><strong>Date:</strong> {c['date'][:10]}</p>
            <p><strong>Weight:</strong> {c['weight']}</p>
            <p><strong>Energy:</strong> {c['energy']}/10</p>
            <p><strong>Goal:</strong> {c['goal']}</p>
            <p><strong>Goal:</strong> {c.get('goal', 'Not set')}</p>
            <p><strong>Sleep:</strong> {c['sleep']}/10</p>
            <p><strong>Nutrition:</strong> {c['nutrition']}/10</p>
            <p><strong>Stress:</strong> {c['stress']}/10</p>
            <p><strong>Win:</strong> {c['win']}</p>
            <p><strong>Struggle:</strong> {c['struggle']}</p>

            {trend_html}

            <p><strong>Coach Note:</strong> {c.get('coach_note', 'None yet')}</p>

            <form method="POST" action="/note/{checkin_id}?password={COACH_PASSWORD}">
                <input name="note" placeholder="Add coach note">
                <button type="submit">Save Note</button>
            </form>
        </div>
        """

        previous = c

    return f"""
    <h1>{client_name}'s Check-In History</h1>

    {summary_html}

    <h3>{weight_change}</h3>

    <a href="{coach_dashboard_link()}">← Back to Dashboard</a>

    {history}
    """


@app.route("/note/<int:checkin_id>", methods=["POST"])
def add_note(checkin_id):
    if not is_coach_logged_in():
        return "Unauthorized."

    checkins = load_checkins()

    if checkin_id < 0 or checkin_id >= len(checkins):
        return "Check-in not found."

    note = request.form.get("note")
    checkins[checkin_id]["coach_note"] = note

    save_checkins(checkins)

    return f"""
    <h1>Coach Note Saved ✅</h1>
    <a href="{coach_dashboard_link()}">Back to Dashboard</a>
    """


@app.route("/search")
def search_clients():
    if not is_coach_logged_in():
        return "Unauthorized"

    query = request.args.get("q", "").lower()
    checkins = load_checkins()

    matches = []

    for c in checkins:
        if query in c["client"].lower():
            matches.append(c["client"])

    unique_matches = sorted(set(matches))
    results = ""

    for client in unique_matches:
        results += f"""
        <li>
            <a href="/client/{client}?password={COACH_PASSWORD}">
                {client}
            </a>
    <br><br>

<a href="/leaderboard?password={COACH_PASSWORD}">
    Client Leaderboard
</a>
        </li>
        """

    return f"""
    <h1>Client Search</h1>

    <form>
        <input type="hidden" name="password" value="{COACH_PASSWORD}">
        <input name="q" placeholder="Search client" value="{query}">
        <button type="submit">Search</button>
    </form>

    <ul>
        {results}
    </ul>

    <a href="{coach_dashboard_link()}">Back to Dashboard</a>
    """

@app.route("/leaderboard")
def leaderboard():
    if not is_coach_logged_in():
        return "Unauthorized"

    checkins = load_checkins()

    counts = {}

    for c in checkins:
        client = c["client"]

        if client not in counts:
            counts[client] = 0

        counts[client] += 1

    sorted_clients = sorted(
        counts.items(),
        key=lambda x: x[1],
        reverse=True
    )

    leaderboard_html = ""

    for rank, (client, total) in enumerate(sorted_clients, start=1):
        leaderboard_html += f"""
        <li>
            #{rank} -
            <a href="/client/{client}?password={COACH_PASSWORD}">
                {client}
            </a>
            ({total} check-ins)
        </li>
        """

    return f"""
    <h1>🏆 Client Leaderboard</h1>

    <ol>
        {leaderboard_html}
    </ol>

    <a href="{coach_dashboard_link()}">
        Back to Dashboard
    </a>
    """

if __name__ == "__main__":
    app.run(debug=True)