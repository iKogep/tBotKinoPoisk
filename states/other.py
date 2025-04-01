from telebot.handler_backends import State, StatesGroup


class OtherState(StatesGroup):
    """ Описывает состояния пользователя в других случаях. """
    # Выбор диапазона дат.
    history_search = State()
    # Выбор номера запроса из списка.
    history_view = State()
    # Перелистывание фильмов в истории.
    history_page = State()
    # Очистка БД
    service_clean = State()
