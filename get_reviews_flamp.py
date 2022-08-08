import json
import requests

with open("settings.json", "r") as settings_file:
    settings = json.load(settings_file)

authorization = "Bearer 2b93f266f6a4df2bb7a196bb76dca60181ea3b37"

link = settings["flamp_reviews_link"]
while True:
    response = requests.get(link, headers={"authorization": authorization}).json()
    # print(response)
    for review in response["reviews"]:
        print(review)
    try:
        link = response["next_link"]
    except KeyError:
        break
