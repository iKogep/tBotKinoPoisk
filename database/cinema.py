import peewee as pw
from config_data.config import DB_PATH


db = pw.SqliteDatabase(DB_PATH)


class BaseModel(pw.Model):
    class Meta:
        database = db


class User(BaseModel):
    """ Описывает представление пользователя. """
    # Первичный ключ, будет совпадать с Telegram ID.
    user_id = pw.IntegerField(primary_key=True)
    # Никнейм в Telegram (может отсутствовать).
    username = pw.CharField(null=True)
    # Имя в Telegram (как отображается в чате).
    first_name = pw.CharField()
    # Фамилия в Telegram. Может быть не указана.
    last_name = pw.CharField(null=True)


class Request(BaseModel):
    """ Описывает представление запроса. """
    # Первичный ключ.
    request_id = pw.AutoField()
    # Внешний ключ запроса, связывающий запрос с пользователем.
    user_id = pw.ForeignKeyField(User, backref='requests')
    # Дата осуществления запроса.
    date = pw.DateField()
    # Содержание запроса. В формате словаря, т.к. поиск может осуществляться по разным реквизитам.
    content = pw.CharField()
    # Ответ на запрос. В формате списка идентификаторов фильмов.
    response = pw.CharField()


class Film(BaseModel):
    """
    Описывает представление фильма.
    Таблица создана для сокращения кол-ва запросов к API, при просмотре истории запросов и перелистывании фильмов.
    """
    # Первичный ключ, будет совпадать с ID фильма на кинопоиске.
    film_id = pw.IntegerField(primary_key=True)
    # Название фильма.
    title = pw.CharField()
    # Описание фильма.
    description = pw.CharField(null=True)
    # Рейтинг фильма.
    rating = pw.FloatField(null=True)
    # Год выхода фильма.
    year = pw.IntegerField(null=True)
    # Жанр фильма.
    genre = pw.CharField(null=True)
    # Возрастное ограничение фильма.
    age = pw.IntegerField(null=True)
    # Ссылка на постер.
    poster_url = pw.CharField(null=True)
    # Дата создания карточки фильма. Необходима при очистке БД.
    date = pw.DateField()

    def __str__(self):
        text = f'{self.title}, год: {self.year}, рейтинг: {self.rating}\n' \
               f'{self.age}+, жанр: {self.genre}\n' \
               f'описание: {self.description}.'
        return text

    def get_simple_data(self) -> dict:
        """ Возвращает основные свойства фильма в виде словаря. """
        data = dict()
        data['film_id'] = self.film_id
        data['title'] = self.title
        data['description'] = self.description
        data['rating'] = self.rating
        data['year'] = self.year
        data['genre'] = self.genre
        data['age'] = self.age
        data['poster_url'] = self.poster_url
        return data


def create_models() -> None:  # Выполняем один раз, для создания файла БД со структурой.
    """ Функция создания БД и структуры БД. Выполняется ВРУЧНУЮ, однократно. """
    db.create_tables(BaseModel.__subclasses__())
