from telebot.handler_backends import State, StatesGroup


class TitleState(StatesGroup):
    """ Описывает состояния пользователя при поиске фильмов по названию. """
    # Ввод названия фильма.
    title = State()
    # Выбор количества результатов поиска.
    count = State()
    # Перелистывание результатов.
    pagination = State()
