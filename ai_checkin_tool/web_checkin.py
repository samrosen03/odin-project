import json
import os
from datetime import datetime

from flask import Flask, request

app = Flask(__name__)

DATA_FILE = "data/checkins.json"


def load_checkins():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_checkins(checkins):
    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w") as f:
        json.dump(checkins, f, indent=2)


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
        <a href="/dashboard">View dashboard</a>
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

        <label>Biggest win this week:</label><br>
        <textarea name="win" required></textarea><br><br>

        <label>Biggest struggle this week:</label><br>
        <textarea name="struggle" required></textarea><br><br>

        <button type="submit">Submit Check-In</button>
    </form>
    """


@app.route("/dashboard")
def dashboard():
    checkins = load_checkins()

    if not checkins:
        return """
        <h1>Coach Dashboard</h1>
        <p>No check-ins yet.</p>
        <a href="/checkin">Go to check-in form</a>
        """

    cards = ""

    for checkin_id, c in reversed(list(enumerate(checkins))):
        status = "✅"

        if (
            int(c["sleep"]) <= 4
            or int(c["stress"]) >= 8
            or int(c["energy"]) <= 4
        ):
            status = "🚨 Needs Attention"

        cards += f"""
        <div style="border:1px solid #ccc; padding:15px; margin:15px 0;">
            <h2>
                <a href="/client/{c['client']}">
                    {c['client']}
                </a>
            </h2>

            <p><strong>Status:</strong> {status}</p>
            <p><strong>Date:</strong> {c['date'][:10]}</p>
            <p><strong>Weight:</strong> {c['weight']}</p>
            <p><strong>Energy:</strong> {c['energy']}/10</p>
            <p><strong>Sleep:</strong> {c['sleep']}/10</p>
            <p><strong>Nutrition:</strong> {c['nutrition']}/10</p>
            <p><strong>Stress:</strong> {c['stress']}/10</p>
            <p><strong>Win:</strong> {c['win']}</p>
            <p><strong>Struggle:</strong> {c['struggle']}</p>

            <p><strong>Coach Note:</strong> {c.get('coach_note', 'None yet')}</p>

            <form method="POST" action="/note/{checkin_id}">
                <input name="note" placeholder="Add coach note">
                <button type="submit">Save Note</button>
            </form>
        </div>
        """

    return f"""
    <h1>Coach Dashboard</h1>
    <p><a href="/checkin">Submit new check-in</a></p>
    {cards}
    """


@app.route("/client/<client_name>")
def client_history(client_name):
    checkins = load_checkins()

    client_checkins = [
        (checkin_id, c)
        for checkin_id, c in enumerate(checkins)
        if c["client"].lower() == client_name.lower()
    ]

    if not client_checkins:
        return f"<h1>No check-ins found for {client_name}</h1>"

    history = ""

    for checkin_id, c in reversed(client_checkins):
        history += f"""
        <div style="border:1px solid #ccc; padding:15px; margin:15px 0;">
            <p><strong>Date:</strong> {c['date'][:10]}</p>
            <p><strong>Weight:</strong> {c['weight']}</p>
            <p><strong>Energy:</strong> {c['energy']}/10</p>
            <p><strong>Sleep:</strong> {c['sleep']}/10</p>
            <p><strong>Nutrition:</strong> {c['nutrition']}/10</p>
            <p><strong>Stress:</strong> {c['stress']}/10</p>
            <p><strong>Win:</strong> {c['win']}</p>
            <p><strong>Struggle:</strong> {c['struggle']}</p>

            <p><strong>Coach Note:</strong> {c.get('coach_note', 'None yet')}</p>

            <form method="POST" action="/note/{checkin_id}">
                <input name="note" placeholder="Add coach note">
                <button type="submit">Save Note</button>
            </form>
        </div>
        """

    return f"""
    <h1>{client_name}'s Check-In History</h1>

    <a href="/dashboard">← Back to Dashboard</a>

    {history}
    """


@app.route("/note/<int:checkin_id>", methods=["POST"])
def add_note(checkin_id):
    checkins = load_checkins()

    if checkin_id < 0 or checkin_id >= len(checkins):
        return "Check-in not found."

    note = request.form.get("note")
    checkins[checkin_id]["coach_note"] = note

    save_checkins(checkins)

    return """
    <h1>Coach Note Saved ✅</h1>
    <a href="/dashboard">Back to Dashboard</a>
    """


if __name__ == "__main__":
    app.run(debug=True)