import json
from .cinema import User, Film, Request
from utils.misc import subtract_days
from config_data.config import DATE_FORMAT


def get_film(film_id: int) -> (str, str):  # Т.к. проект учебный, то этот блок имеет место быть.
    """
    Возвращает из БД информацию о фильме по его идентификатору.
    Возвращает описание фильма в формате строки, а также отдельно ссылку на постер.
    :param film_id: int - идентификатор фильма.
    :return: кортеж из двух строк.
    """
    film = Film.get_or_none(Film.film_id == film_id)
    # Название фильма есть всегда.
    text = f'{film.title}'
    # Год выпуска может быть нулевым.
    if film.year > 0:
        text += f' [{film.year} год]'
    # Данные о возрастном ограничении могут отсутствовать.
    if film.age is not None:
        text += f' {film.age}+'
    # Жанр может быть пустым.
    if film.genre != '':
        text += f'\nЖанр: {film.genre}'
    # Рейтинг может быть нулевым.
    if film.rating > 0:
        text += f', рейтинг: {film.rating}.'
    else:
        text += '.'
    # Поле с описанием может быть пустым.
    if (film.description is not None) and (film.description != ''):
        text += f'\nОписание: {film.description}'
    # Лимит длины поля caption команды send_photo 1024 символа.
    if len(text) > 1024:
        text = text[:1024]
    # Корректность ссылки будет проверена при загрузке.
    poster_url = film.poster_url
    return text, poster_url


def get_requests(user_id: int, dt: str) -> list:
    """
    Возвращает из БД все запросы пользователя сделанные в указанную дату или период.
    Дата принимается в одном из двух форматов: '01.01.2025' или '01.01.2025-10.01.2025'.
    Возвращает список запросов (не более 99), где каждый запрос представлен в виде словаря.
    Данный словарь содержит как содержимое запроса пользователя, так и полученный ответ (список фильмов).
    :param user_id: int идентификатор пользователя.
    :param dt: str дата (диапазон дат).
    :return: список словарей.
    """
    user = User.get_or_none(User.user_id == user_id)
    if len(dt) == 10:
        # Ограничение выдачи 99 запросов, так как у инлайн-клавиатуры лимит 100 кнопок: 99 запросов + кнопка возврата.
        request = user.requests.where(Request.user_id == user_id, Request.date == dt).limit(99)
    else:
        request = user.requests.where(Request.user_id == user_id,
                                      Request.date >= dt[:10],
                                      Request.date <= dt[11:]).limit(99)

    request_list = []

    for i_elem in request:
        # Каждый запрос преобразуем в словарь и добавляем его в список.
        request_list.append({'request_id': i_elem.request_id,
                             'user_id': i_elem.user_id,
                             'date': i_elem.date,
                             'content': json.loads(i_elem.content),
                             'response': json.loads(i_elem.response)})

    return request_list


def get_history(user_id: int, dt: str) -> (str, dict):
    """
    Формирует список запросов пользователя за указанную дату или период в виде строки,
    а также список ответов в виде словаря. В тексте запросы пронумерованы, в словаре ключи ответов имеют теже номера.
    :param user_id: int идентификатор пользователя.
    :param dt: дата или диапазон дат.
    :return: кортеж из строки и словаря.
    """
    request_list = get_requests(user_id=user_id, dt=dt)
    resp_dict = dict()

    if len(request_list) == 0:
        return f'В указанный {"день" if len(dt) == 10 else "период"} вы ничего не искали.', resp_dict
    else:
        text_content = f'В указанный {"день" if len(dt) == 10 else "период"} вы искали:'

    for index in range(len(request_list)):
        idx = index + 1
        i_dict = request_list[index]['content']

        if 'title' in i_dict:
            i_result = f'{idx}. {i_dict["title"].capitalize()}.'
        elif 'genre' in i_dict:
            i_result = f'{idx}. {i_dict["genre"].capitalize()} ({i_dict["rating"]}).'
        else:
            i_result = ''

        text_content += f'\n{i_result} Найдено фильмов: {len(request_list[index]["response"])}.'
        resp_dict[idx] = request_list[index]['response']

    text_content += '\nДля просмотра результатов запроса, выберите его номер из списка.'

    return text_content, resp_dict


def get_stat_info() -> str:
    """
    Возвращает из БД статистическую информацию о количестве записей в таблицах.
    :return: строка.
    """
    users_count = User.select().count()
    requests_count = Request.select().count()
    films_count = Film.select().count()
    result = 'Таблица пользователей содержит записей: {}.\n' \
             'Таблица запросов содержит записей: {}.\n' \
             'Таблица фильмов содержит записей: {}.'.format(users_count, requests_count, films_count)
    return result


def clear_base() -> str:
    """
    Осуществляет удаление из БД запросов старше 30 дней, а также фильмов, на которые нет ссылок в оставшихся запросах.
    Возвращает строку, в которой содержится информация о количестве удаленных записей из таблиц БД.
    :return: строка.
    """
    target_day = subtract_days(30)
    full_set_id = set()
    # Получаем множество фильмов, которые содержатся в старых запросах (под удаление).
    query = Request.select(Request.response).where(Request.date <= target_day.strftime(DATE_FORMAT))
    query.execute()

    for i_query in query:
        list_id = json.loads(i_query.response)
        for i_elem in list_id:
            full_set_id.add(i_elem)

    # Удаляем старые запросы.
    query = Request.delete().where(Request.date <= target_day.strftime(DATE_FORMAT))
    deleted_requests = query.execute()
    # Получаем множество фильмов, которые содержатся в оставшихся запросах.
    query = Request.select(Request.response).execute()
    temp_set_id = set()

    for i_query in query:
        list_id = json.loads(i_query.response)
        for i_elem in list_id:
            temp_set_id.add(i_elem)

    # Получаем множество фильмов подлежащих удалению (не содержатся в оставшихся запросах).
    full_set_id.difference_update(temp_set_id)

    # Удаляем лишние фильмы.
    for i_elem in full_set_id:
        query = Film.delete().where(Film.film_id == i_elem)
        query.execute()

    result = 'Очистка БД завершена.\n' \
             'Из таблицы запросов удалено записей: {}.\n' \
             'Из таблицы фильмов удалено записей: {}.'.format(deleted_requests, len(full_set_id))
    return result
