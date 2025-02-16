import json
import requests

USERNAME = "almsam"
TOKEN = "GITH_TOKEN"  # if needed


def fetch_current_stats():
    current_contributions = 10
    current_streak = 30
    return current_contributions, current_streak

def load_previous_stats(filepath="stats.json"):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"contributions": 0, "streak": 0}

def save_current_stats(stats, filepath="stats.json"):
    with open(filepath, "w") as f:
        json.dump(stats, f, indent=2)
