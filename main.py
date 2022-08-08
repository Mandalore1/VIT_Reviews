import requests
import json


def handle_reviews_2gis(reviews, firm_id):
    """Сохраняет отзывы из полученного массива отзывов. В источник подставляется ссылка на обзоры конкретной фирмы."""
    source = f"https://2gis.ru/ufa/branches/2393074172953395/firm/{firm_id}/tab/reviews"
    for review in reviews:
        user_name = review["user"]["name"]
        date_created = review["date_created"]
        rating = review["rating"]
        text = review["text"]
        with open("reviews_2gis.txt", "a", encoding="utf-8") as file:
            file.write(f"{user_name}, {date_created}, {rating}, {text}, {source}\n")


def handle_firms_2gis(firms):
    """Сохраняет отзывы для каждой фирмы 'Вкусно и точка'"""
    for firm in firms:
        # Берем id фирмы и формируем ссылку на данные об отзывах о фирме
        firm_id = firm["id"].split("_")[0]
        link = settings["2gis_reviews_link_head"] + str(firm_id) + settings["2gis_reviews_link_tail"]

        # В цикле последовательно получаем информацию об отзывах
        response = requests.get(link).json()
        while True:
            # Сохраняем информацию
            handle_reviews_2gis(response["reviews"], firm_id)

            # Ссылка на следующую порцию отзывов в атрибуте meta.next
            try:
                next_link = response["meta"]["next_link"]
            except KeyError:
                break

            response = requests.get(next_link).json()


with open("settings.json", "r") as settings_file:
    settings = json.load(settings_file)

# Забираем информацию о фирмах
# С User-Agent Mozilla Firefox работает
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"
response = requests.get(settings["2gis_firms_link"], headers={"User-Agent": user_agent}).json()

firms = response["result"]["items"]
handle_firms_2gis(firms)
