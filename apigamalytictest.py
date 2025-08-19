import requests

API_KEY = "ZuUHpZK8Be2zKt1PzrBwQ1Kg7dRCuCYI"
game_id = 570
url = f"https://api.gamalytic.com/game/{game_id}"
headers = {
    "Accept": "application/json",
    "X-API-Key": API_KEY
}

response = requests.get(url, headers=headers)
response.raise_for_status()
game = response.json()
print(game)
