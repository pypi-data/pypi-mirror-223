import requests


def get_data(town_name):
    url = "https://rearthserver.net/map/"
    response = requests.get(url, allow_redirects=True)
    redirected_url = response.url
    endpoint_url = f"{redirected_url}tiles/_markers_/marker_world.json"
    response = requests.get(endpoint_url)
    data = response.json()
    town_data = data["sets"]["towny.markerset"]["areas"][f"{town_name}__0"]
    return town_data
