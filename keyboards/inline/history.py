from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from config_data.config import DATE_FORMAT
from utils.misc import subtract_days


def date_key():
    """
    Создает инлайн клавиатуру формата [сегодня, вчера], [три дня, неделя], [2 недели, месяц].
    Шаблон возврата содержит дату (диапазоны дат), которую можно сразу использовать в поисковом запросе.
    :return: клавиатура.
    """
    pattern_1 = 'date#{}'
    pattern_2 = 'date#{}-{}'
    today = datetime.today()
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_1 = InlineKeyboardButton(text='сегодня',
                                    callback_data=pattern_1.format(today.strftime(DATE_FORMAT)))
    button_2 = InlineKeyboardButton(text='вчера',
                                    callback_data=pattern_1.format(subtract_days(1).strftime(DATE_FORMAT)))
    keyboard.add(button_1, button_2, row_width=2)
    button_1 = InlineKeyboardButton(text='три дня',
                                    callback_data=pattern_2.format(subtract_days(2).strftime(DATE_FORMAT),
                                                                   today.strftime(DATE_FORMAT)))
    button_2 = InlineKeyboardButton(text='неделя',
                                    callback_data=pattern_2.format(subtract_days(6).strftime(DATE_FORMAT),
                                                                   today.strftime(DATE_FORMAT)))
    keyboard.add(button_1, button_2, row_width=2)
    button_1 = InlineKeyboardButton(text='две недели',
                                    callback_data=pattern_2.format(subtract_days(13).strftime(DATE_FORMAT),
                                                                   today.strftime(DATE_FORMAT)))
    button_2 = InlineKeyboardButton(text='месяц',
                                    callback_data=pattern_2.format(subtract_days(29).strftime(DATE_FORMAT),
                                                                   today.strftime(DATE_FORMAT)))
    keyboard.add(button_1, button_2, row_width=2)
    keyboard.add(InlineKeyboardButton(text='назад', callback_data='key_back#0'))
    return keyboard


def history_key(count: int, pattern: str = 'hist#{}'):
    """
    Создает инлайн клавиатуру для просмотра истории запросов.
    Клавиатура состоит из пронумерованных кнопок от 1 до 99 и кнопки возврата.
    В один ряд можно вывести до 8 кнопок.
    :param count: общее количество кнопок, без учета кнопки возврата.
    :param pattern: шаблон для возвращаемого значения.
    :return: клавиатура.
    """
    if count > 99:
        count = 99
    elif count < 0:
        count = 0

    whole = count // 8
    remains = count % 8
    keyboard = InlineKeyboardMarkup(row_width=3)

    for index in range(1, 8 * whole, 8):
        keyboard.add(InlineKeyboardButton(text='{}'.format(index + 0), callback_data=pattern.format(index + 0)),
                     InlineKeyboardButton(text='{}'.format(index + 1), callback_data=pattern.format(index + 1)),
                     InlineKeyboardButton(text='{}'.format(index + 2), callback_data=pattern.format(index + 2)),
                     InlineKeyboardButton(text='{}'.format(index + 3), callback_data=pattern.format(index + 3)),
                     InlineKeyboardButton(text='{}'.format(index + 4), callback_data=pattern.format(index + 4)),
                     InlineKeyboardButton(text='{}'.format(index + 5), callback_data=pattern.format(index + 5)),
                     InlineKeyboardButton(text='{}'.format(index + 6), callback_data=pattern.format(index + 6)),
                     InlineKeyboardButton(text='{}'.format(index + 7), callback_data=pattern.format(index + 7)),
                     row_width=8)

    start = 8 * whole + 1
    if remains == 7:
        keyboard.add(InlineKeyboardButton(text='{}'.format(start + 0), callback_data=pattern.format(start + 0)),
                     InlineKeyboardButton(text='{}'.format(start + 1), callback_data=pattern.format(start + 1)),
                     InlineKeyboardButton(text='{}'.format(start + 2), callback_data=pattern.format(start + 2)),
                     InlineKeyboardButton(text='{}'.format(start + 3), callback_data=pattern.format(start + 3)),
                     InlineKeyboardButton(text='{}'.format(start + 4), callback_data=pattern.format(start + 4)),
                     InlineKeyboardButton(text='{}'.format(start + 5), callback_data=pattern.format(start + 5)),
                     InlineKeyboardButton(text='{}'.format(start + 6), callback_data=pattern.format(start + 6)),
                     row_width=remains)
    elif remains == 6:
        keyboard.add(InlineKeyboardButton(text='{}'.format(start + 0), callback_data=pattern.format(start + 0)),
                     InlineKeyboardButton(text='{}'.format(start + 1), callback_data=pattern.format(start + 1)),
                     InlineKeyboardButton(text='{}'.format(start + 2), callback_data=pattern.format(start + 2)),
                     InlineKeyboardButton(text='{}'.format(start + 3), callback_data=pattern.format(start + 3)),
                     InlineKeyboardButton(text='{}'.format(start + 4), callback_data=pattern.format(start + 4)),
                     InlineKeyboardButton(text='{}'.format(start + 5), callback_data=pattern.format(start + 5)),
                     row_width=remains)
    elif remains == 5:
        keyboard.add(InlineKeyboardButton(text='{}'.format(start + 0), callback_data=pattern.format(start + 0)),
                     InlineKeyboardButton(text='{}'.format(start + 1), callback_data=pattern.format(start + 1)),
                     InlineKeyboardButton(text='{}'.format(start + 2), callback_data=pattern.format(start + 2)),
                     InlineKeyboardButton(text='{}'.format(start + 3), callback_data=pattern.format(start + 3)),
                     InlineKeyboardButton(text='{}'.format(start + 4), callback_data=pattern.format(start + 4)),
                     row_width=remains)
    elif remains == 4:
        keyboard.add(InlineKeyboardButton(text='{}'.format(start + 0), callback_data=pattern.format(start + 0)),
                     InlineKeyboardButton(text='{}'.format(start + 1), callback_data=pattern.format(start + 1)),
                     InlineKeyboardButton(text='{}'.format(start + 2), callback_data=pattern.format(start + 2)),
                     InlineKeyboardButton(text='{}'.format(start + 3), callback_data=pattern.format(start + 3)),
                     row_width=remains)
    elif remains == 3:
        keyboard.add(InlineKeyboardButton(text='{}'.format(start + 0), callback_data=pattern.format(start + 0)),
                     InlineKeyboardButton(text='{}'.format(start + 1), callback_data=pattern.format(start + 1)),
                     InlineKeyboardButton(text='{}'.format(start + 2), callback_data=pattern.format(start + 2)),
                     row_width=remains)
    elif remains == 2:
        keyboard.add(InlineKeyboardButton(text='{}'.format(start + 0), callback_data=pattern.format(start + 0)),
                     InlineKeyboardButton(text='{}'.format(start + 1), callback_data=pattern.format(start + 1)),
                     row_width=remains)
    elif remains == 1:
        keyboard.add(InlineKeyboardButton(text='{}'.format(start + 0), callback_data=pattern.format(start + 0)),
                     row_width=remains)

    keyboard.add(InlineKeyboardButton(text='назад', callback_data='key_back#0'))
    return keyboard
