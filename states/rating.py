from telebot.handler_backends import State, StatesGroup


class RatingState(StatesGroup):
    """ Описывает состояния пользователя при поиске фильмов по рейтингу. """
    # Выбор жанра фильма.
    genre = State()
    # Ввод рейтинга (диапазона).
    rating = State()
    # Выбор количества результатов.
    count = State()
    # Перелистывание результатов.
    pagination = State()
