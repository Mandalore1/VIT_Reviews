import requests
import json
import db


def handle_reviews_2gis(reviews, firm_id):
    """
    Сохраняет отзывы из полученного списка отзывов. В источник подставляется ссылка на обзоры конкретной фирмы.

    :param reviews: Список отзывов
    :param firm_id: Id в 2gis текущей фирмы "Вкусно и точка"
    """
    source = f"https://2gis.ru/ufa/branches/2393074172953395/firm/{firm_id}/tab/reviews"
    for review_data in reviews:
        review = dict()
        review["source"] = source
        review["user_name"] = review_data["user"]["name"]
        review["date_created"] = review_data["date_created"]
        review["rating"] = review_data["rating"]
        review["text"] = review_data["text"]
        db.save_review_to_database(review)

        # with open("reviews_2gis.txt", "a", encoding="utf-8") as file:
        #     file.write(f"{user_name}, {date_created}, {rating}, {text}, {source}\n")


def handle_firms_2gis(firms, settings):
    """
    Сохраняет отзывы для каждой фирмы 'Вкусно и точка'

    :param firms: Список фирм
    :param settings: Словарь настроек из settings.json
    """
    for firm in firms:
        # Берем id фирмы и формируем ссылку на данные об отзывах о фирме
        firm_id = firm["id"].split("_")[0]
        link = settings["2gis_reviews_link_head"] + str(firm_id) + settings["2gis_reviews_link_tail"]

        # В цикле последовательно получаем информацию об отзывах
        response = requests.get(link).json()
        while True:
            # Сохраняем информацию
            handle_reviews_2gis(response["reviews"], firm_id)

            # Ссылка на следующую порцию отзывов в атрибуте meta.next_link JSON-файла
            try:
                next_link = response["meta"]["next_link"]
            except KeyError:
                break

            response = requests.get(next_link).json()


def main():
    with open("settings.json", "r") as settings_file:
        settings = json.load(settings_file)

    # Соединяемся с базой данных
    db.init_database()

    # Забираем информацию о фирмах
    # С User-Agent Mozilla Firefox работает, с Google Chrome почему-то не работает
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"
    response = requests.get(settings["2gis_firms_link"], headers={"User-Agent": user_agent}).json()

    # Информация о фирмах в result.items JSON-файла
    firms = response["result"]["items"]
    handle_firms_2gis(firms, settings)

    # Закрываем базу данных
    db.close_connection()


if __name__ == "__main__":
    main()
