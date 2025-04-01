import re
from datetime import datetime


def checking_rating_format(string: str) -> bool:
    """
    Проверяет соответствие строки формату поискового запроса для рейтинга фильма.
    :param string: str - строка.
    :return: bool - результат проверки - Истина / Ложь.
    """
    text = string.strip()
    if text.isdecimal():
        if 1 <= int(text) <= 10:
            return True
    if re.fullmatch(r'\d-\d{1,2}', text):
        a, b = int(text[0]), int(text[2:])
        if (a >= 1) and (b <= 10) and (a < b):
            return True
    return False


def checking_date_correct(string: str) -> bool:
    """
    Проверяет, является ли строка корректной датой.
    :param string: str - строка, которая проверяется на соответствие формату.
    :return: bool - результат проверки - Истина / Ложь.
    """
    try:
        date_obj = datetime.strptime(string, '%d.%m.%Y').date()
        return True
    except ValueError:
        return False


def checking_date_format(string: str) -> bool:
    """
    Проверяет, является ли строка корректной для поиска по дате.
    :param string: str - строка, которая проверяется на соответствие формату.
    :return: bool - результат проверки - Истина / Ложь.
    """
    text = string.strip()
    if re.fullmatch(r'\d\d.\d\d.\d{4}', text):
        if checking_date_correct(text):
            return True
    if re.fullmatch(r'\d\d.\d\d.\d{4}-\d\d.\d\d.\d{4}', text):
        if checking_date_correct(text[:10]) and checking_date_correct(text[11:]):
            return True
    return False
