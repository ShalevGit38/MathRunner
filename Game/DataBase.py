import requests

# Your Firebase Realtime Database URL (ends with .json)
db_url = 'https://mathrunner-62d5d-default-rtdb.firebaseio.com/'

def save_score(player_name, score):
    data = {
        "name": player_name,
        "score": score
    }
    response = requests.post(db_url + 'scores.json', json=data)
    print("Saved:", response.json())

def get_scores():
    response = requests.get(db_url + 'scores.json')
    scores = response.json()
    if scores:
        for key, entry in scores.items():
            print(f"{entry['name']} - {entry['score']}")
    else:
        print("No scores found.")

get_scores()
