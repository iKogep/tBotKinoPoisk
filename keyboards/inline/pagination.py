from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def mark_button(number, current, pattern_current, pattern_cb):
    """
    Создает кнопку на основе двух шаблонов в зависимости от того, является ли она текущей или нет.
    :param number: номер кнопки.
    :param current: номер текущей кнопки, то есть той которую нужно отметить.
    :param pattern_current: шаблон для кнопки, являющейся текущей (отмеченной).
    :param pattern_cb: шаблон для обычной кнопки.
    :return: кнопка.
    """
    if number == current:
        button = InlineKeyboardButton(text=pattern_current.format(number),
                                      callback_data=pattern_cb.format(page=number))
    else:
        button = InlineKeyboardButton(text='{}'.format(number),
                                      callback_data=pattern_cb.format(page=number))
    return button


def pagination_keys(page_count: int,
                    page_current: int,
                    data_pattern: str = '{page}',
                    back_key: int = 0
                    ) -> InlineKeyboardMarkup:
    """
    Создает инфлайн клавиатуру для перелистывания списка сообщений.
    :param page_count: общее количество кнопок (страниц для перелистывания), без учета кнопки возврата.
    :param page_current: номер текущей страницы.
    :param data_pattern: шаблон для возврата значений.
    :param back_key: номер кнопки возврата (позволяет регулировать вложенные меню).
    :return: клавиатура.
    """
    pattern_first_page_label = '⏮️ {}'
    pattern_previous_page_label = '⏪ {}'
    pattern_current_page_label = '[{}]'
    pattern_next_page_label = '{} ⏩'
    pattern_last_page_label = '{} ⏭️'
    pattern_back_key_label = 'key_back#{}'

    if page_current < 1:
        page_current = 1
    elif page_current > page_count:
        page_current = page_count

    if page_count == 1:
        keyboard = InlineKeyboardMarkup(row_width=1)
    elif 2 <= page_count <= 5:
        keyboard = InlineKeyboardMarkup(row_width=page_count)
        button = dict()

        for index in range(1, page_count + 1):
            button[index] = mark_button(number=index, current=page_current,
                                        pattern_current=pattern_current_page_label, pattern_cb=data_pattern)

        if page_count == 2:
            keyboard.add(button[1], button[2], row_width=page_count)
        elif page_count == 3:
            keyboard.add(button[1], button[2], button[3], row_width=page_count)
        elif page_count == 4:
            keyboard.add(button[1], button[2], button[3], button[4], row_width=page_count)
        else:
            keyboard.add(button[1], button[2], button[3], button[4], button[5], row_width=page_count)

    elif page_current <= 3:  # 1 2 3 4 max
        keyboard = InlineKeyboardMarkup(row_width=5)
        button = dict()

        for index in range(1, 5):
            button[index] = mark_button(number=index, current=page_current,
                                        pattern_current=pattern_current_page_label, pattern_cb=data_pattern)

        button[5] = InlineKeyboardButton(text=pattern_last_page_label.format(page_count),
                                         callback_data=data_pattern.format(page=page_count))
        keyboard.add(button[1], button[2], button[3], button[4], button[5])
    elif page_current >= page_count - 2:  # 1 max--- max-- max- max
        keyboard = InlineKeyboardMarkup(row_width=5)
        button = dict()
        button[1] = InlineKeyboardButton(text=pattern_first_page_label.format(1),
                                         callback_data=data_pattern.format(page=1))
        button[2] = mark_button(number=page_count - 3, current=page_current,
                                pattern_current=pattern_current_page_label, pattern_cb=data_pattern)
        button[3] = mark_button(number=page_count - 2, current=page_current,
                                pattern_current=pattern_current_page_label, pattern_cb=data_pattern)
        button[4] = mark_button(number=page_count - 1, current=page_current,
                                pattern_current=pattern_current_page_label, pattern_cb=data_pattern)
        button[5] = mark_button(number=page_count, current=page_current,
                                pattern_current=pattern_current_page_label, pattern_cb=data_pattern)
        keyboard.add(button[1], button[2], button[3], button[4], button[5], row_width=5)
    else:  # 1 cur- cur cur+ max
        keyboard = InlineKeyboardMarkup(row_width=5)
        button = dict()
        button[1] = InlineKeyboardButton(text=pattern_first_page_label.format(1),
                                         callback_data=data_pattern.format(page=1))
        button[2] = InlineKeyboardButton(text=pattern_previous_page_label.format(page_current - 1),
                                         callback_data=data_pattern.format(page=page_current - 1))
        button[3] = InlineKeyboardButton(text=pattern_current_page_label.format(page_current),
                                         callback_data=data_pattern.format(page=page_current))
        button[4] = InlineKeyboardButton(text=pattern_next_page_label.format(page_current + 1),
                                         callback_data=data_pattern.format(page=page_current + 1))
        button[5] = InlineKeyboardButton(text=pattern_last_page_label.format(page_count),
                                         callback_data=data_pattern.format(page=page_count))
        keyboard.add(button[1], button[2], button[3], button[4], button[5], row_width=5)

    # Кнопка возврата добавляется в конце.
    button_back = InlineKeyboardButton(text='назад', callback_data=pattern_back_key_label.format(back_key))
    keyboard.add(button_back, row_width=1)

    return keyboard
