from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def service_key():
    """
    Создает инлайн клавиатуру с кнопкой очистки БД и возврата.
    :return: клавиатура.
    """
    pattern = 'service#{}'
    keyboard = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text='очистить БД', callback_data=pattern.format(0))
    keyboard.add(button, row_width=1)
    keyboard.add(InlineKeyboardButton(text='назад', callback_data='key_back#0'))
    return keyboard
