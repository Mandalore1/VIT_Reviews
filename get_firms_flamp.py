import json
import requests

with open("settings.json", "r") as settings_file:
    settings = json.load(settings_file)

authorization = "Bearer 2b93f266f6a4df2bb7a196bb76dca60181ea3b37"
firms = []

link = settings["flamp_firms_link"]
while True:
    response = requests.get(link, headers={"authorization": authorization}).json()
    # print(response)
    firms += response["filials"]
    try:
        link = response["next_link"]
    except KeyError:
        break

for firm in firms:
    firm_id = firm["id"]
    print(firm_id)
