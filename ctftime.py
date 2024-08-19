import requests
from datetime import datetime

current_year = datetime.now().year

print('''

  /$$$$$$  /$$$$$$$$ /$$$$$$$$ /$$$$$$$$ /$$$$$$ /$$      /$$ /$$$$$$$$       /$$$$$$$$ /$$$$$$   /$$$$$$  /$$      
 /$$__  $$|__  $$__/| $$_____/|__  $$__/|_  $$_/| $$$    /$$$| $$_____/      |__  $$__//$$__  $$ /$$__  $$| $$      
| $$  \__/   | $$   | $$         | $$     | $$  | $$$$  /$$$$| $$               | $$  | $$  \ $$| $$  \ $$| $$      
| $$         | $$   | $$$$$      | $$     | $$  | $$ $$/$$ $$| $$$$$            | $$  | $$  | $$| $$  | $$| $$      
| $$         | $$   | $$__/      | $$     | $$  | $$  $$$| $$| $$__/            | $$  | $$  | $$| $$  | $$| $$      
| $$    $$   | $$   | $$         | $$     | $$  | $$\  $ | $$| $$               | $$  | $$  | $$| $$  | $$| $$      
|  $$$$$$/   | $$   | $$         | $$    /$$$$$$| $$ \/  | $$| $$$$$$$$         | $$  |  $$$$$$/|  $$$$$$/| $$$$$$$$
 \______/    |__/   |__/         |__/   |______/|__/     |__/|________/         |__/   \______/  \______/ |________/
                                                                                                                 
''')

team_id = input("Enter the team ID: ")
team_id = int(team_id)

team_info_url = f"https://ctftime.org/api/v1/teams/{team_id}/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

team_response = requests.get(team_info_url, headers=headers)

if team_response.status_code == 200:
    team_data = team_response.json()
    print("Team Information:")
    print(f"Name: {team_data['name']}")
    print(f"Primary Alias: {team_data['primary_alias']}")
    current_year_str = str(current_year)
    country_place = team_data.get('rating', {}).get(current_year_str, {}).get('country_place', 'N/A')
    print(f"Country Place: {country_place}")
    rating = team_data.get('rating', {}).get(current_year_str, {}).get('rating_points', 'N/A')
    if rating != 'N/A':
        rating = round(rating, 2)
    print(f"Rating: {rating}")
    print(f"Country: {team_data['country']}\n")

    # Continue with results retrieval
    results_url = f"https://ctftime.org/api/v1/results/{current_year}/"
    results_response = requests.get(results_url, headers=headers)

    if results_response.status_code == 200:
        results_data = results_response.json()
        events = []
        for event_id, event in results_data.items():
            for score in event['scores']:
                if score['team_id'] == team_id:
                    points = float(score['points'])
                    if points.is_integer():
                        points = int(points)
                    try:
                        event_time = datetime.fromtimestamp(float(event['time']))
                    except (TypeError, ValueError):
                        print(f"Error parsing time for event {event['title']}: {event['time']}")
                        event_time = datetime.min
                    events.append({
                        'title': event['title'].strip(),
                        'points': points,
                        'time': event_time
                    })
        events.sort(key=lambda x: x['time'], reverse=False)
        print("CTF Results for 2024 (Oldest to Newest):")
        for event in events:
            print(f"CTF Name: {event['title']}, Points: {event['points']}")
    else:
        print(f"Failed to retrieve CTF results. Status code: {results_response.status_code}")
else:
    print(f"Failed to retrieve team information. Status code: {team_response.status_code}")
