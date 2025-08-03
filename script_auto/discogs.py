import requests


def item_user(username,token):
  url = f"https://api.discogs.com/users/{username}/collection/folders/0/releases"
  headers = {"Authorization": f"Discogs token={token}","User-Agent": "User-inventory/1.0" }

  response = requests.get(url, headers=headers)

  if response.status_code == 200:
    data = response.json()
    total_items = data.get('pagination', {}).get('items', 0)
    print(f"L'utilisateur {username} a {total_items} item(s) dans sa collection.")
    return total_items
  else:
    print(f"Erreur {response.status_code} : {response.text}")