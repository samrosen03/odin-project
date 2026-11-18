import json
import os
from datetime import datetime

from flask import Flask, render_template, request, session, redirect
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


DATA_FILE = "data/checkins.json"
WORKOUT_FILE = "data/workouts.json"
COACH_PASSWORD = os.getenv("COACH_PASSWORD")

if not app.secret_key:
    raise RuntimeError(
        "SECRET_KEY is missing. Add it to your .env file."
    )

if not COACH_PASSWORD:
    raise RuntimeError(
        "COACH_PASSWORD is missing. Add it to your .env file."
    )


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
    return session.get("coach_logged_in") is True

