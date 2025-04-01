import requests
from config_data.config import KP_API_KEY, SITE_BASE


def get_genre() -> list:
    """
    Получает от сервера список жанров, необходимый для поиска по рейтингу.
    Если сервер не вернул список жанров, то используется автономный список (по состоянию на январь 2025 года.)
    :return: list(str) - список жанров.
    """
    response = requests.get(f'{SITE_BASE}/v1/movie/possible-values-by-field',
                            params={'field': 'genres.name'},
                            headers={'X-API-KEY': KP_API_KEY})

    if response.status_code != 200:
        print(f'Не удалось получить список жанров. Будет использован автономный список. Ошибка {response.status_code}.')
        genres = [
            {"name": "аниме", "slug": "anime"}, {"name": "биография", "slug": "biografiya"},
            {"name": "боевик", "slug": "boevik"}, {"name": "вестерн", "slug": "vestern"},
            {"name": "военный", "slug": "voennyy"}, {"name": "детектив", "slug": "detektiv"},
            {"name": "детский", "slug": "detskiy"}, {"name": "для взрослых", "slug": "dlya-vzroslyh"},
            {"name": "документальный", "slug": "dokumentalnyy"}, {"name": "драма", "slug": "drama"},
            {"name": "игра", "slug": "igra"}, {"name": "история", "slug": "istoriya"},
            {"name": "комедия", "slug": "komediya"}, {"name": "концерт", "slug": "koncert"},
            {"name": "короткометражка", "slug": "korotkometrazhka"}, {"name": "криминал", "slug": "kriminal"},
            {"name": "мелодрама", "slug": "melodrama"}, {"name": "музыка", "slug": "muzyka"},
            {"name": "мультфильм", "slug": "multfilm"}, {"name": "мюзикл", "slug": "myuzikl"},
            {"name": "новости", "slug": "novosti"}, {"name": "приключения", "slug": "priklyucheniya"},
            {"name": "реальное ТВ", "slug": "realnoe-TV"}, {"name": "семейный", "slug": "semeynyy"},
            {"name": "спорт", "slug": "sport"}, {"name": "ток-шоу", "slug": "tok-shou"},
            {"name": "триллер", "slug": "triller"}, {"name": "ужасы", "slug": "uzhasy"},
            {"name": "фантастика", "slug": "fantastika"}, {"name": "фильм-нуар", "slug": "film-nuar"},
            {"name": "фэнтези", "slug": "fentezi"}, {"name": "церемония", "slug": "ceremoniya"}
        ]
        return genres

    genres = response.json()
    result = []

    for i_dict in genres:
        result.append(i_dict['name'])

    return result


def search_movie_by_id(kp_id: int) -> requests.Response:
    """
    Получает с сайта информацию о фильме по его идентификатору.
    :param kp_id: int Идентификатор фильма.
    :return: ответ сайта.
    """
    response = requests.get(f'{SITE_BASE}v1.4/movie/{kp_id}', headers={'X-API-KEY': KP_API_KEY})
    return response


def search_movie_by_title(title: str, limit: int) -> requests.Response:
    """
    Получает с сайта информацию о limit фильмах название которых соответствует title.
    :param title: str - название (ключевое слово) фильма, который ищем.
    :param limit: int - ограничение числа возвращаемых результатов.
    :return: ответ сайта.
    """
    response = requests.get(f'{SITE_BASE}v1.4/movie/search',
                            params={'page': 1, 'limit': limit, 'query': title},
                            headers={'X-API-KEY': KP_API_KEY})
    return response


def search_movie_by_rating(genre: str, rating: str, limit: int) -> requests.Response:
    """
    Получает с сайта информацию о limit фильмах соответствующих жанру genre и имеющих рейтинг rating.
    :param genre: str - жанр фильма.
    :param rating: str - рейтинг (диапазон) фильма.
    :param limit: int - ограничение числа возвращаемых результатов.
    :return: ответ сайта.
    """
    response = requests.get(f'{SITE_BASE}v1.4/movie',
                            params={'sortField': 'rating.kp', 'sortType': -1, 'genres.name': genre,
                                    'rating.kp': rating, 'page': 1, 'limit': limit},
                            headers={'X-API-KEY': KP_API_KEY})
    return response
