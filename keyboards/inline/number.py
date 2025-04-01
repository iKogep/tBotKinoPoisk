from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def number_keys(num_dict: dict) -> InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру для выбора количества ответов.
    Кнопки создаются на основе словаря.
    Возвращает клавиатуру.
    """
    keyboard = InlineKeyboardMarkup(row_width=5)
    button = dict()
    for index in range(1, 11):  # todo переделать на текстовые
        button[index] = InlineKeyboardButton(text='{}'.format(index * 10), callback_data=num_dict[index])
    keyboard.add(button[1], button[2], button[3], button[4], button[5])
    keyboard.add(button[6], button[7], button[8], button[9], button[10])

    return keyboard
