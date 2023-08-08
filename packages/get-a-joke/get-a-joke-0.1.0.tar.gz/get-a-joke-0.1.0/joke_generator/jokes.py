import requests


def get_joke_by_type(joke_type):
    api_url = f"https://v2.jokeapi.dev/joke/{joke_type}"
    response = requests.get(api_url)

    if response.status_code == 200:
        joke_data = response.json()
        if joke_data["type"] == "single":
            return joke_data["joke"]
        elif joke_data["type"] == "twopart":
            return f"{joke_data['setup']} {joke_data['delivery']}"
        else:
            return "No joke found."
    else:
        return "Failed to fetch joke."
