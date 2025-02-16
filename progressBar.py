import json
import requests
import os
from datetime import datetime, timedelta

TOKEN = os.environ.get("GITHUB_TOKEN") #initally an environ variable for tonek was to be declared, instead we use this
if not TOKEN: TOKEN = "" # print("GH token not found apperently")

USERNAME = "almsam"


def load_previous_stats(filepath="stats.json"):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"contributions": -1, "streak": -1}

def save_current_stats(stats, filepath="stats.json"):
    with open(filepath, "w") as f:
        json.dump(stats, f, indent=2)

def compare_stats(old, new):
    diff_contributions = new["contributions"] - old["contributions"]
    diff_streak = new["streak"] - old["streak"]
    return diff_contributions, diff_streak

def compute_streak(weeks):
    contributions = {}
    for week in weeks:
        for day in week['contributionDays']:
            # Map each date (YYYY-MM-DD) to its contribution count
            contributions[day['date']] = day['contributionCount']
    
    # Use UTC date since GitHub's API is in UTC
    streak = 0
    current_date = datetime.utcnow().date()
    
    while True:
        date_str = current_date.strftime("%Y-%m-%d")
        # If the date is not in our data, assume no contributions (or break if we've exhausted the range)
        count = contributions.get(date_str, 0)
        if count > 0:
            streak += 1
        else:
            break
        current_date -= timedelta(days=1)
    
    return streak

def fetch_current_stats(username, token):
    # GitHub's GraphQL
    url = "https://api.github.com/graphql"
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """
    variables = {"login": username}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    if response.status_code != 200: raise Exception(f"GraphQL query failed, inf: {response.status_code}: {response.text}")
    
    data = response.json()
    calendar = data['data']['user']['contributionsCollection']['contributionCalendar']; total_contributions = calendar['totalContributions']
    weeks = calendar['weeks']; current_streak = compute_streak(weeks)
    
    return total_contributions, current_streak

def main():
    curr_contribs, curr_streak = fetch_current_stats(USERNAME, TOKEN)
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
