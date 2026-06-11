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
        <ul>
            {feedback_html}
        </ul>

        <p><strong>Main Focus:</strong> {checkin_data['struggle']}</p>

        <br>
        <a href="/checkin">Submit another check-in</a>
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


if __name__ == "__main__":
    app.run(debug=True)