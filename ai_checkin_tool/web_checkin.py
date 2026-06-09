from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>AI Check-In Tool is running ✅</h1>
    <p>Go to <a href="/checkin">/checkin</a> to submit a check-in.</p>
    """


@app.route("/checkin", methods=["GET", "POST"])
def checkin():
    if request.method == "POST":
        client = request.form.get("client")
        weight = request.form.get("weight")
        energy = request.form.get("energy")
        sleep = request.form.get("sleep")
        nutrition = request.form.get("nutrition")
        stress = request.form.get("stress")
        win = request.form.get("win")
        struggle = request.form.get("struggle")

        return f"""
        <h1>Check-in Submitted ✅</h1>
        <p><strong>Client:</strong> {client}</p>
        <p><strong>Weight:</strong> {weight}</p>
        <p><strong>Energy:</strong> {energy}/10</p>
        <p><strong>Sleep:</strong> {sleep}/10</p>
        <p><strong>Nutrition:</strong> {nutrition}/10</p>
        <p><strong>Stress:</strong> {stress}/10</p>
        <p><strong>Win:</strong> {win}</p>
        <p><strong>Struggle:</strong> {struggle}</p>

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