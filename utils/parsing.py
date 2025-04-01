import datetime
import requests
from peewee import IntegrityError
from database.cinema import Film
from config_data.config import DATE_FORMAT


def parsing_movie(data_dict: dict) -> int:
    """
    Парсит данные одного фильма. Сохраняет данные о фильме в БД. Возвращает ID фильма.
    :param data_dict: dict - полная информация о фильме в формате сайта.
    :return: int - идентификатор фильма.
    """
    parsing_result = dict()
    parsing_result['film_id'] = int(data_dict['id'])
    parsing_result['date'] = datetime.date.today().strftime(DATE_FORMAT)

    if ((data_dict["name"] is not None) and (data_dict["alternativeName"] is not None) and
            (len(data_dict["name"]) > 0) and (len(data_dict["alternativeName"]) > 0)):
        title = f'{data_dict["name"]} ({data_dict["alternativeName"]})'
    elif (data_dict["name"] is not None) and (len(data_dict["name"]) > 0):
        title = data_dict["name"]
    elif (data_dict["alternativeName"] is not None) and (len(data_dict["alternativeName"]) > 0):
        title = data_dict["alternativeName"]
    else:
        title = 'Ошибка сайта'

    parsing_result['title'] = title
    parsing_result['description'] = data_dict['description']
    parsing_result['rating'] = data_dict['rating']['kp']
    parsing_result['year'] = data_dict['year']
    genre = ''

    for i_elem in data_dict['genres']:
        genre += f'{i_elem["name"]}, '

    genre = genre.strip()
    genre = genre.strip(',')
    parsing_result['genre'] = genre
    parsing_result['age'] = data_dict['ageRating']

    # Попадались фильмы без этого поля, то есть с нарушенной структурой ответа.
    try:
        parsing_result['poster_url'] = data_dict['poster']['url']
    except KeyError:
        parsing_result['poster_url'] = None

    try:
        Film.create(**parsing_result)
    except IntegrityError:
        pass  # Фильм уже есть в базе.

    return parsing_result['film_id']


def parsing_response(response: requests.Response) -> list:
    """
    Парсит ответ сайта, разбивая его на фильмы. Возвращает список идентификаторов фильмов.
    :param response: ответ сайта.
    :return: список фильмов (идентификаторов).
    """
    if response.status_code != 200:
        return []

    temp_dict = response.json()
    temp_list = temp_dict['docs']
    result = []

    for i_dict in temp_list:
        result.append(parsing_movie(data_dict=i_dict))

    return result
