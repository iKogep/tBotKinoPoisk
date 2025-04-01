from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def genre_keys(genres: list) -> InlineKeyboardMarkup:
    """
    Создает инлайн клавиатуру.
    Проходит по списку. Для каждого элемента списка создает кнопку и добавляет её к клавиатуре.
    Атрибуты:
        genres: list - список направлений перевода.
    Возвращает клавиатуру.
    """
    keyboard = InlineKeyboardMarkup(row_width=2)
    index = 0

    while len(genres) - index >= 2:
        button_1 = InlineKeyboardButton(text=genres[index], callback_data=genres[index])
        button_2 = InlineKeyboardButton(text=genres[index + 1], callback_data=genres[index + 1])
        keyboard.add(button_1, button_2)
        index += 2

    if len(genres) - index == 1:
        button_1 = InlineKeyboardButton(text=genres[index], callback_data=genres[index])
        keyboard.add(button_1)
        index += 1

    return keyboard
