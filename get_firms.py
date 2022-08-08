import json
import requests

with open("settings.json", "r") as settings_file:
    settings = json.load(settings_file)

# С User-Agent Mozilla Firefox работает
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"
response = requests.get(settings["2gis_firms_link"], headers={"User-Agent": user_agent}).json()
print(response)

firms = response["result"]["items"]

for firm in firms:
    firm_id = firm["id"].split("_")[0]
    print(firm_id)
