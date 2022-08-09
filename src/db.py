import os

import peewee
from datetime import datetime

import pytz

db = peewee.PostgresqlDatabase(database=os.environ.get("DATABASE_NAME"),
                               user=os.environ.get("DATABASE_USER"),
                               password=os.environ.get("DATABASE_PASSWORD"),
                               host=os.environ.get("DATABASE_HOST"))


class Review(peewee.Model):
    """Модель отзыва"""
    source = peewee.CharField()
    user_name = peewee.CharField()
    date_created = peewee.DateTimeField()
    rating = peewee.IntegerField()
    text = peewee.TextField()

    class Meta:
        database = db


class LastRun(peewee.Model):
    """Последние запуски программы"""
    datetime = peewee.DateTimeField()

    class Meta:
        database = db


def init_database():
    """Инициализирует базу данных"""
    db.connect()

    # Если таблиц еще нет, они будут созданы, существующие таблицы не изменятся
    db.create_tables([LastRun, Review])


def close_connection():
    """Закрывает соединение"""
    db.close()


def save_review_to_database(review):
    """
    Сохраняет отзыв в базе данных

    :param review: Словарь из source, user_name, date_created, rating, text
    """
    Review.create(**review)


def get_last_run_datetime():
    """Возвращает дату и время последнего запуска с часовым поясом +5 Уфа. Если запусков не было, возвращает 2000 год"""
    try:
        last_run = LastRun.select().order_by(LastRun.datetime.desc()).limit(1).get().datetime

        last_run = last_run.replace(tzinfo=pytz.timezone("Asia/Yekaterinburg"))
    except peewee.DoesNotExist:
        last_run = datetime.fromisoformat("2000-01-01T00:00:00+05:00")

    return last_run


def save_last_run_datetime(last_run):
    """
    Сохраняет время последнего запуска

    :param last_run: Время последнего запуска
    """
    LastRun.create(datetime=last_run)


def get_reviews_by_date(min_date, max_date=None, desc=False, limit=10):
    """Выдает максимум limit отзывов с датой между min_date и max_date. По умолчанию по возрастанию"""
    if not max_date:
        max_date = datetime.now()

    reviews = Review.select().where(Review.date_created > min_date, Review.date_created < max_date).limit(limit)

    if desc:
        reviews = reviews.order_by(Review.date_created.desc())
    else:
        reviews = reviews.order_by(Review.date_created.asc())

    return reviews
