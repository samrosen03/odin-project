
import json
import os
from datetime import datetime

from flask import Flask, render_template, request

app = Flask(__name__)

DATA_FILE = "data/checkins.json"
WORKOUT_FILE = "data/workouts.json"
COACH_PASSWORD = "coach123"


def load_checkins():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_checkins(checkins):
    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w") as file:
        json.dump(checkins, file, indent=2)


def load_workouts():
    if not os.path.exists(WORKOUT_FILE):
        return []

    with open(WORKOUT_FILE, "r") as file:
        return json.load(file)


def save_workouts(workouts):
    os.makedirs("data", exist_ok=True)

    with open(WORKOUT_FILE, "w") as file:
        json.dump(workouts, file, indent=2)


def check_for_new_pr(client_name, exercise, weight):
    workouts = load_workouts()

    try:
        new_weight = float(weight)
    except (ValueError, TypeError):
        return False

    previous_weights = []

    for workout in workouts:
        same_client = (
            workout.get("client", "").strip().lower()
            == client_name.strip().lower()
        )
        same_exercise = (
            workout.get("exercise", "").strip().lower()
            == exercise.strip().lower()
        )

        if not (same_client and same_exercise):
            continue

        try:
            previous_weights.append(float(workout.get("weight", "")))
        except (ValueError, TypeError):
            continue

    if not previous_weights:
        return True

    return new_weight > max(previous_weights)


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
        feedback.append(
            "Great job staying consistent with your nutrition this week."
        )

    if energy >= 7:
        feedback.append(
            "Your energy looks solid, which is a good sign your routine is supporting you."
        )

    if sleep <= 5:
        feedback.append(
            "Sleep looks like the biggest opportunity this week. "
            "Aim to improve your bedtime routine and recovery."
        )

    if stress >= 7:
        feedback.append(
            "Stress is elevated, so focus on recovery, hydration, walks, "
            "and keeping training manageable."
        )

    if energy <= 5:
        feedback.append(
            "Energy is low, so avoid trying to crush every workout. "
            "Focus on consistency and recovery."
        )

    if not feedback:
        feedback.append(
            "Overall, this looks like a steady week. Keep building consistency "
            "and focus on one small improvement."
        )

    return feedback


def generate_action_items(checkin):
    actions = []

    if int(checkin["sleep"]) <= 5:
        actions.append("😴 Prioritize getting at least 7-8 hours of sleep.")

    if int(checkin["nutrition"]) <= 6:
        actions.append(
            "🥗 Focus on hitting your nutrition goals 5+ days this week."
        )

    if int(checkin["stress"]) >= 7:
        actions.append("🧘 Schedule at least one recovery activity this week.")

    if int(checkin["energy"]) <= 5:
        actions.append("🏃 Reduce training intensity and focus on recovery.")

    if not actions:
        actions.append("✅ Stay consistent with your current routine.")

    return actions


def recommend_workout(checkin):
    energy = int(checkin["energy"])
    stress = int(checkin["stress"])
    sleep = int(checkin["sleep"])

    if energy <= 4 or sleep <= 4 or stress >= 8:
        return (
            "🟢 Recovery Week: Walk, mobility work, and light strength training."
        )

    if energy >= 8 and stress <= 4:
        return "🔥 Push Week: Train hard and increase weights if possible."

    return "💪 Normal Week: Stay consistent and complete your planned workouts."


def calculate_compliance_score(checkin):
    score = (
        int(checkin["energy"])
        + int(checkin["sleep"])
        + int(checkin["nutrition"])
        + (11 - int(checkin["stress"]))
    )

    return round(score / 40 * 100)


def calculate_risk_level(checkin):
    energy = int(checkin["energy"])
    sleep = int(checkin["sleep"])
    stress = int(checkin["stress"])

    if sleep <= 4 or energy <= 4 or stress >= 8:
        return "High", "#dc2626"

    if sleep <= 6 or stress >= 6:
        return "Moderate", "#f59e0b"

    return "Low", "#16a34a"


def build_trend_html(current, previous):
    if not previous:
        return ""

    metrics = ["energy", "sleep", "nutrition", "stress"]
    trend_html = "<h4>📈 Progress Since Last Check-In</h4><ul>"

    for metric in metrics:
        difference = int(current[metric]) - int(previous[metric])

        if difference > 0:
            trend_html += f"<li>{metric.title()}: +{difference}</li>"
        elif difference < 0:
            trend_html += f"<li>{metric.title()}: {difference}</li>"
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
    except (ValueError, TypeError):
        return "Weight Change: Invalid weight data"

    change = latest_weight - first_weight

    if change > 0:
        return f"⬆️ Weight Change: +{change:.1f} lbs"

    if change < 0:
        return f"⬇️ Weight Change: {change:.1f} lbs"

    return "➡️ Weight Change: No Change"


def build_client_summary(client_checkins):
    total = len(client_checkins)

    avg_energy = round(
        sum(int(item[1]["energy"]) for item in client_checkins) / total,
        1,
    )
    avg_sleep = round(
        sum(int(item[1]["sleep"]) for item in client_checkins) / total,
        1,
    )
    avg_nutrition = round(
        sum(int(item[1]["nutrition"]) for item in client_checkins) / total,
        1,
    )
    avg_stress = round(
        sum(int(item[1]["stress"]) for item in client_checkins) / total,
        1,
    )

    latest = client_checkins[-1][1]

    return f"""
    <h2>📊 Client Summary</h2>

    <p><strong>Total Check-Ins:</strong> {total}</p>
    <p><strong>Current Goal:</strong> {latest.get('goal', 'Not set')}</p>
    <p><strong>Average Energy:</strong> {avg_energy}/10</p>
    <p><strong>Average Sleep:</strong> {avg_sleep}/10</p>
    <p><strong>Average Nutrition:</strong> {avg_nutrition}/10</p>
    <p><strong>Average Stress:</strong> {avg_stress}/10</p>

    <p><strong>Latest Win:</strong> {latest['win']}</p>
    <p><strong>Latest Struggle:</strong> {latest['struggle']}</p>

    <hr>
    """


def build_recent_prs(client_name):
    workouts = load_workouts()

    client_prs = [
        workout
        for workout in workouts
        if workout["client"].lower() == client_name.lower()
        and workout.get("is_pr")
    ]

    if not client_prs:
        return """
        <h2>⭐ Recent PRs</h2>
        <p>No PRs logged yet.</p>
        """

    prs_html = "<h2>⭐ Recent PRs</h2>"

    for personal_record in reversed(client_prs[-5:]):
        prs_html += f"""
        <div class="card">
            <p><strong>Date:</strong> {personal_record['date'][:10]}</p>
            <p><strong>Exercise:</strong> {personal_record['exercise']}</p>
            <p><strong>Weight:</strong> {personal_record['weight']}</p>
            <p><strong>Reps:</strong> {personal_record['reps']}</p>
        </div>
        """

    return prs_html


def build_pr_table(client_name):
    workouts = load_workouts()
    personal_records = {}

    for workout in workouts:
        if workout["client"].lower() != client_name.lower():
            continue

        if not workout.get("is_pr"):
            continue

        exercise = workout["exercise"]
        personal_records[exercise] = workout

    if not personal_records:
        return """
        <h2>🏆 Current Personal Records</h2>
        <p>No PRs yet.</p>
        """

    table_html = """
    <h2>🏆 Current Personal Records</h2>

    <table border="1" cellpadding="8">
        <tr>
            <th>Exercise</th>
            <th>Best Lift</th>
        </tr>
    """

    for exercise, personal_record in sorted(personal_records.items()):
        table_html += f"""
        <tr>
            <td>{exercise}</td>
            <td>{personal_record['weight']} × {personal_record['reps']}</td>
        </tr>
        """

    table_html += "</table><br>"
    return table_html


def build_attendance_streak(client_checkins):
    total = len(client_checkins)

    if total == 1:
        return "🔥 1 Check-In"

    return f"🔥 {total} Check-Ins"


def build_workout_history(client_name):
    workouts = load_workouts()

    client_workouts = [
        workout
        for workout in workouts
        if workout["client"].lower() == client_name.lower()
    ]

    if not client_workouts:
        return """
        <h2>🏋️ Workout History</h2>
        <p>No workouts logged yet.</p>
        """

    workout_html = "<h2>🏋️ Workout History</h2>"

    for workout in reversed(client_workouts):
        pr_badge = " ⭐ PR" if workout.get("is_pr") else ""

        workout_html += f"""
        <div class="card">
            <p><strong>Date:</strong> {workout['date'][:10]}</p>
            <p>
                <strong>Exercise:</strong>
                {workout['exercise']}{pr_badge}
            </p>
            <p><strong>Weight:</strong> {workout['weight']}</p>
            <p><strong>Reps:</strong> {workout['reps']}</p>
            <p><strong>Notes:</strong> {workout.get('notes', '')}</p>
        </div>
        """

    return workout_html


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/checkin", methods=["GET", "POST"])
def checkin():
    if request.method == "POST":
        checkin_data = {
            "date": datetime.now().isoformat(),
            "client": request.form.get("client", "").strip(),
            "weight": request.form.get("weight", "").strip(),
            "goal": request.form.get("goal", "").strip(),
            "energy": request.form.get("energy", "").strip(),
            "sleep": request.form.get("sleep", "").strip(),
            "nutrition": request.form.get("nutrition", "").strip(),
            "stress": request.form.get("stress", "").strip(),
            "win": request.form.get("win", "").strip(),
            "struggle": request.form.get("struggle", "").strip(),
            "coach_note": "",
        }

        checkins = load_checkins()
        checkins.append(checkin_data)
        save_checkins(checkins)

        feedback = generate_coach_feedback(checkin_data)
        actions = generate_action_items(checkin_data)
        workout_recommendation = recommend_workout(checkin_data)
        compliance = calculate_compliance_score(checkin_data)

        feedback_html = "".join(
            f"<li>{item}</li>"
            for item in feedback
        )
        actions_html = "".join(
            f"<li>{item}</li>"
            for item in actions
        )

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

        <hr>

        <h2>📋 Action Plan for This Week</h2>
        <ul>{actions_html}</ul>

        <hr>

        <h2>🏋️ Workout Recommendation</h2>
        <p>{workout_recommendation}</p>

        <hr>

        <h2>📈 Weekly Compliance Score</h2>

        <div class="progress-container">
            <div
                class="progress-bar"
                style="width:{compliance}%;">
            </div>
        </div>

        <h2>{compliance}%</h2>

        <p>
            <strong>Main Focus:</strong>
            {checkin_data['struggle']}
        </p>

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

        <label>Primary Goal:</label><br>
        <select name="goal" required>
            <option value="">Select Goal</option>
            <option>Lose Fat</option>
            <option>Build Muscle</option>
            <option>Improve Strength</option>
            <option>Improve Endurance</option>
            <option>General Health</option>
        </select><br><br>

        <label>Energy 1-10:</label><br>
        <input
            name="energy"
            type="number"
            min="1"
            max="10"
            required>
        <br><br>

        <label>Sleep 1-10:</label><br>
        <input
            name="sleep"
            type="number"
            min="1"
            max="10"
            required>
        <br><br>

        <label>Nutrition 1-10:</label><br>
        <input
            name="nutrition"
            type="number"
            min="1"
            max="10"
            required>
        <br><br>

        <label>Stress 1-10:</label><br>
        <input
            name="stress"
            type="number"
            min="1"
            max="10"
            required>
        <br><br>

        <label>Biggest win this week:</label><br>
        <textarea name="win" required></textarea><br><br>

        <label>Biggest struggle this week:</label><br>
        <textarea name="struggle" required></textarea><br><br>

        <button type="submit">Submit Check-In</button>
    </form>
    """


@app.route("/workout", methods=["GET", "POST"])
def workout_logger():
    if not is_coach_logged_in():
        return """
        <h1>Coach Login</h1>

        <form method="GET" action="/workout">
            <input
                name="password"
                type="password"
                placeholder="Coach password">

            <button type="submit">Login</button>
        </form>
        """

    selected_client = request.args.get("client", "").strip()

    if request.method == "POST":
        client_name = request.form.get("client", "").strip()
        exercise = request.form.get("exercise", "").strip()
        weight = request.form.get("weight", "").strip()
        reps = request.form.get("reps", "").strip()
        notes = request.form.get("notes", "").strip()

        is_pr = check_for_new_pr(
            client_name,
            exercise,
            weight,
        )

        workout_data = {
            "date": datetime.now().isoformat(),
            "client": client_name,
            "exercise": exercise,
            "weight": weight,
            "reps": reps,
            "is_pr": is_pr,
            "notes": notes,
        }

        workouts = load_workouts()
        workouts.append(workout_data)
        save_workouts(workouts)

        return f"""
        <h1>Workout Saved ✅</h1>

        <p><strong>Client:</strong> {workout_data['client']}</p>
        <p><strong>Exercise:</strong> {workout_data['exercise']}</p>
        <p><strong>Weight:</strong> {workout_data['weight']}</p>
        <p><strong>Reps:</strong> {workout_data['reps']}</p>
        <p>
            <strong>PR:</strong>
            {"Yes" if workout_data['is_pr'] else "No"}
        </p>
        <p><strong>Notes:</strong> {workout_data['notes']}</p>

        <br>

        <a
            href="/workout?password={COACH_PASSWORD}&client={workout_data['client']}">
            Log another workout for {workout_data['client']}
        </a>
        <br>

        <a
            href="/client/{workout_data['client']}?password={COACH_PASSWORD}">
            View client profile
        </a>
        <br>

        <a href="{coach_dashboard_link()}">
            Back to Dashboard
        </a>
        """

    return f"""
    <h1>Log Workout</h1>

    <form
        method="POST"
        action="/workout?password={COACH_PASSWORD}&client={selected_client}">

        <label>Client Name:</label><br>

        <input
            name="client"
            value="{selected_client}"
            required>
        <br><br>

        <label>Exercise:</label><br>

        <select name="exercise" required>
            <option value="">Select Exercise</option>
            <option>Trap Bar Deadlift</option>
            <option>Bench Press</option>
            <option>Goblet Squat</option>
            <option>Push-Up</option>
            <option>Pull-Up</option>
            <option>Farmer Carry</option>
            <option>Plank</option>
            <option>Row</option>
            <option>Other</option>
        </select>
        <br><br>

        <label>Weight:</label><br>
        <input name="weight" required><br><br>

        <label>Reps:</label><br>
        <input name="reps" required><br><br>

        <label>Notes:</label><br>
        <textarea name="notes"></textarea><br><br>

        <button type="submit">Save Workout</button>
    </form>

    <br>

    <a href="{coach_dashboard_link()}">
        Back to Dashboard
    </a>
    """


@app.route("/dashboard")
def dashboard():
    if not is_coach_logged_in():
        return """
        <h1>Coach Login</h1>

        <form method="GET" action="/dashboard">
            <input
                name="password"
                type="password"
                placeholder="Coach password">

            <button type="submit">Login</button>
        </form>
        """

    checkins = load_checkins()
    cards = ""

    total_checkins = len(checkins)
    clients = sorted(
        set(checkin["client"] for checkin in checkins)
    )
    total_clients = len(clients)

    follow_up = sum(
        1
        for checkin in checkins
        if (
            datetime.now()
            - datetime.fromisoformat(checkin["date"])
        ).days >= 7
    )

    leaderboard = {}

    for checkin in checkins:
        client = checkin["client"]
        leaderboard[client] = leaderboard.get(client, 0) + 1

    most_active = "-"

    if leaderboard:
        most_active = max(
            leaderboard,
            key=leaderboard.get,
        )

    stats_html = f"""
    <div class="stats-bar">
        <div class="stat-card">
            <h3>👥 Clients</h3>
            <p>{total_clients}</p>
        </div>

        <div class="stat-card">
            <h3>📝 Check-Ins</h3>
            <p>{total_checkins}</p>
        </div>

        <div class="stat-card">
            <h3>🚨 Follow-Ups</h3>
            <p>{follow_up}</p>
        </div>

        <div class="stat-card">
            <h3>🏆 Most Active</h3>
            <p>{most_active}</p>
        </div>
    </div>
    """

    if not checkins:
        return f"""
        <h1>Coach Dashboard</h1>

        <p>No check-ins yet.</p>

        <p>
            <a href="/checkin">
                Submit new check-in
            </a>
        </p>

        <p>
            <a href="/workout?password={COACH_PASSWORD}">
                Log Workout
            </a>
        </p>

        <p>
            <a href="/search?password={COACH_PASSWORD}">
                Search Clients
            </a>
        </p>

        <p>
            <a href="/leaderboard?password={COACH_PASSWORD}">
                Client Leaderboard
            </a>
        </p>

        {stats_html}
        """

    for checkin_id, checkin in reversed(
        list(enumerate(checkins))
    ):
        risk, color = calculate_risk_level(checkin)

        checkin_date = datetime.fromisoformat(checkin["date"])
        days_since = (datetime.now() - checkin_date).days

        followup = ""

        if days_since >= 7:
            followup = " 🚨 Follow Up"

        cards += f"""
        <div class="card">
            <h2>
                <a
                    href="/client/{checkin['client']}?password={COACH_PASSWORD}">
                    {checkin['client']}
                </a>
            </h2>

            <p>
                <strong>Risk Level:</strong>

                <span
                    style="
                        background:{color};
                        color:white;
                        padding:6px 12px;
                        border-radius:20px;
                        font-weight:bold;
                    ">
                    {risk}
                </span>
            </p>

            <p>
                <strong>Last Check-In:</strong>
                {days_since} day(s) ago{followup}
            </p>

            <p><strong>Date:</strong> {checkin['date'][:10]}</p>
            <p><strong>Weight:</strong> {checkin['weight']}</p>
            <p>
                <strong>Goal:</strong>
                {checkin.get('goal', 'Not set')}
            </p>
            <p><strong>Energy:</strong> {checkin['energy']}/10</p>
            <p><strong>Sleep:</strong> {checkin['sleep']}/10</p>
            <p>
                <strong>Nutrition:</strong>
                {checkin['nutrition']}/10
            </p>
            <p><strong>Stress:</strong> {checkin['stress']}/10</p>
            <p><strong>Win:</strong> {checkin['win']}</p>
            <p><strong>Struggle:</strong> {checkin['struggle']}</p>

            <p>
                <strong>Coach Note:</strong>
                {checkin.get('coach_note', 'None yet')}
            </p>

            <form
                method="POST"
                action="/note/{checkin_id}?password={COACH_PASSWORD}">

                <input
                    name="note"
                    placeholder="Add coach note">

                <button type="submit">
                    Save Note
                </button>
            </form>
        </div>
        """

    return f"""
    <h1>Coach Dashboard</h1>

    <p><a href="/checkin">Submit new check-in</a></p>

    <p>
        <a href="/workout?password={COACH_PASSWORD}">
            Log Workout
        </a>
    </p>

    <p>
        <a href="/search?password={COACH_PASSWORD}">
            Search Clients
        </a>
    </p>

    <p>
        <a href="/leaderboard?password={COACH_PASSWORD}">
            Client Leaderboard
        </a>
    </p>

    {stats_html}

    {cards}
    """


@app.route("/client/<client_name>")
def client_history(client_name):
    if not is_coach_logged_in():
        return """
        <h1>Coach Login</h1>

        <form method="GET">
            <input
                name="password"
                type="password"
                placeholder="Coach password">

            <button type="submit">
                Login
            </button>
        </form>
        """

    checkins = load_checkins()

    client_checkins = [
        (checkin_id, checkin)
        for checkin_id, checkin in enumerate(checkins)
        if checkin["client"].lower() == client_name.lower()
    ]

    if not client_checkins:
        return f"""
        <h1>No check-ins found for {client_name}</h1>
        <a href="{coach_dashboard_link()}">
            Back to Dashboard
        </a>
        """

    weight_change = calculate_weight_change(client_checkins)
    attendance = build_attendance_streak(client_checkins)
    summary_html = build_client_summary(client_checkins)
    workout_history = build_workout_history(client_name)
    recent_prs = build_recent_prs(client_name)
    pr_table = build_pr_table(client_name)
    latest = client_checkins[-1][1]

    profile_header = f"""
    <div class="profile-header">
        <div class="profile-avatar">
            {latest['client'][0].upper()}
        </div>

        <div>
            <h1>{latest['client']}</h1>

            <p>
                🎯 Goal:
                <strong>{latest.get('goal', 'Not Set')}</strong>
            </p>

            <p>
                ⚖️ Current Weight:
                <strong>{latest['weight']} lbs</strong>
            </p>

            <p>
                <strong>{attendance}</strong>
            </p>
        </div>
    </div>
    """

    history = ""
    previous = None

    for checkin_id, checkin in reversed(client_checkins):
        trend_html = build_trend_html(checkin, previous)

        history += f"""
        <div class="card">
            <p><strong>Date:</strong> {checkin['date'][:10]}</p>
            <p><strong>Weight:</strong> {checkin['weight']}</p>
            <p>
                <strong>Goal:</strong>
                {checkin.get('goal', 'Not set')}
            </p>
            <p><strong>Energy:</strong> {checkin['energy']}/10</p>
            <p><strong>Sleep:</strong> {checkin['sleep']}/10</p>
            <p>
                <strong>Nutrition:</strong>
                {checkin['nutrition']}/10
            </p>
            <p><strong>Stress:</strong> {checkin['stress']}/10</p>
            <p><strong>Win:</strong> {checkin['win']}</p>
            <p><strong>Struggle:</strong> {checkin['struggle']}</p>

            {trend_html}

            <p>
                <strong>Coach Note:</strong>
                {checkin.get('coach_note', 'None yet')}
            </p>

            <form
                method="POST"
                action="/note/{checkin_id}?password={COACH_PASSWORD}">

                <input
                    name="note"
                    placeholder="Add coach note">

                <button type="submit">
                    Save Note
                </button>
            </form>
        </div>
        """

        previous = checkin

    return f"""
    {profile_header}

    {summary_html}

    <h3>{weight_change}</h3>

    <p>
        <a
            href="/workout?password={COACH_PASSWORD}&client={latest['client']}">
            + Log Workout for {latest['client']}
        </a>
    </p>

    <a href="{coach_dashboard_link()}">
        ← Back to Dashboard
    </a>

    <hr>

    {pr_table}

    <hr>

    {recent_prs}

    <hr>

    {workout_history}

    <hr>

    <h2>✅ Check-In History</h2>

    {history}
    """


@app.route("/note/<int:checkin_id>", methods=["POST"])
def add_note(checkin_id):
    if not is_coach_logged_in():
        return "Unauthorized.", 401

    checkins = load_checkins()

    if checkin_id < 0 or checkin_id >= len(checkins):
        return "Check-in not found.", 404

    note = request.form.get("note", "").strip()
    checkins[checkin_id]["coach_note"] = note

    save_checkins(checkins)

    return f"""
    <h1>Coach Note Saved ✅</h1>

    <a href="{coach_dashboard_link()}">
        Back to Dashboard
    </a>
    """


@app.route("/search")
def search_clients():
    if not is_coach_logged_in():
        return "Unauthorized.", 401

    query = request.args.get("q", "").strip().lower()
    checkins = load_checkins()

    matches = []

    for checkin in checkins:
        if query in checkin["client"].lower():
            matches.append(checkin["client"])

    unique_matches = sorted(set(matches))
    results = ""

    for client in unique_matches:
        results += f"""
        <li>
            <a href="/client/{client}?password={COACH_PASSWORD}">
                {client}
            </a>
        </li>
        """

    return f"""
    <h1>Client Search</h1>

    <form>
        <input
            type="hidden"
            name="password"
            value="{COACH_PASSWORD}">

        <input
            name="q"
            placeholder="Search client"
            value="{query}">

        <button type="submit">
            Search
        </button>
    </form>

    <ul>
        {results}
    </ul>

    <p>
        <a href="/leaderboard?password={COACH_PASSWORD}">
            Client Leaderboard
        </a>
    </p>

    <a href="{coach_dashboard_link()}">
        Back to Dashboard
    </a>
    """


@app.route("/leaderboard")
def leaderboard():
    if not is_coach_logged_in():
        return "Unauthorized.", 401

    checkins = load_checkins()
    counts = {}

    for checkin in checkins:
        client = checkin["client"]
        counts[client] = counts.get(client, 0) + 1

    sorted_clients = sorted(
        counts.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    leaderboard_html = ""

    for rank, (client, total) in enumerate(
        sorted_clients,
        start=1,
    ):
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