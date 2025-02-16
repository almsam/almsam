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

def compare_stats(old, new):
    diff_contributions = new["contributions"] - old["contributions"]
    diff_streak = new["streak"] - old["streak"]
    return diff_contributions, diff_streak

def main():
    curr_contribs, curr_streak = fetch_current_stats()
    new_stats = {"contributions": curr_contribs, "streak": curr_streak}
    
    prev_stats = load_previous_stats()

    diff_contribs, diff_streak = compare_stats(prev_stats, new_stats)

    markdown = f"""
### My current goals:

- **Contributions:** {new_stats['contributions']}/2000 (Change: {diff_contribs:+})
- **Streak:** {new_stats['streak']}/365 (Change: {diff_streak:+})
"""
    print(markdown)

    save_current_stats(new_stats)

if __name__ == "__main__":
    main()
