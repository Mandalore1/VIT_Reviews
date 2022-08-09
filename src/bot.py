import os
from datetime import datetime

import telebot
import requests

import db

TOKEN = os.environ.get("TELEBOT_TOKEN")

DEFAULT_MESSAGE = """
Бот посылает максимум 10 сообщений, чтобы не забивать чат!

/new: Получить новые отзывы
/from <дата>: Получить отзывы с определенной даты
/interval <дата начала> <дата конца>: Получить отзывы в определенном интервале
"""

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, DEFAULT_MESSAGE)

    elif message.text.startswith("/from"):
        date = message.text[6:]

        try:
            date = datetime.strptime(date, "%d.%m.%Y")
        except:
            bot.send_message(message.from_user.id, "Дата введена неправильно! Дата должна быть в формате дд.мм.гггг!")
            return

        bot.send_message(message.from_user.id, f"Отзывы с даты {date.date()}")
        for review in get_reviews(date):
            bot.send_message(message.from_user.id, get_review_text(review))

    elif message.text.startswith("/interval"):
        try:
            text = message.text.split(" ")
            min_date = datetime.strptime(text[1], "%d.%m.%Y")
            max_date = datetime.strptime(text[2], "%d.%m.%Y")
        except:
            bot.send_message(message.from_user.id, "Дата введена неправильно! Дата должна быть в формате дд.мм.гггг!")
            return

        bot.send_message(message.from_user.id, f"Отзывы с даты {min_date.date()} до {max_date.date()}")
        for review in get_reviews(min_date, max_date):
            bot.send_message(message.from_user.id, get_review_text(review))

    elif message.text == "/new":
        # Возвращает отзывы с датой после предпоследнего запуска парсера (когда они были загружены)
        try:
            pre_last_run = db.LastRun.select().order_by(db.LastRun.datetime.desc()).limit(2)[1].datetime
        except:
            bot.send_message(message.from_user.id, "Что-то пошло не так!")
            return

        bot.send_message(message.from_user.id, f"Отзывы с {pre_last_run}")
        for review in get_reviews(pre_last_run, desc=True):
            bot.send_message(message.from_user.id, get_review_text(review))

    else:
        bot.send_message(message.from_user.id, "Я тебя не понял. Напиши /help для просмотра списка доступных команд")


def get_review_text(review):
    """Выдает отзыв в виде текста"""
    text = f"Источник: {review.source}\n"
    text += f"Отзыв от: {review.user_name}.\n"
    text += f"Дата: {review.date_created}. Рейтинг: {review.rating}.\n"
    text += f"Текст: {review.text}\n"
    return text


def get_reviews(min_date, max_date=None, desc=False):
    """Получает отзывы с min_date до max_date (по умолчанию текущая дата). По умолчанию по возрастанию."""
    return db.get_reviews_by_date(min_date, max_date, desc)


if __name__ == "__main__":
    db.init_database()
    bot.infinity_polling()
    db.close_connection()
