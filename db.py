import peewee

db = peewee.PostgresqlDatabase(database='reviews', user='reviews_user', password='reviews', host='localhost')


class Review(peewee.Model):
    source = peewee.CharField()
    user_name = peewee.CharField()
    date_created = peewee.DateTimeField()
    rating = peewee.IntegerField()
    text = peewee.TextField()

    class Meta:
        database = db


def init_database():
    """Инициализирует базу данных"""
    db.connect()
    db.create_tables([Review])


def close_connection():
    """Закрывает соединение"""
    db.close()


def save_review_to_database(review):
    """
    Сохраняет отзыв в базе данных

    :param review: Словарь из source, user_name, date_created, rating, text
    """
    Review.create(**review)
