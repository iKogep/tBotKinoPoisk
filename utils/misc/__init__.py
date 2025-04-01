import requests
from datetime import datetime, timedelta


def download_image(url: str) -> requests.Response.content:
    """
    Скачивает изображение по ссылке и возвращает его.
    Если изображение не скачивается, то скачивает и возвращает картинку об отсутствии постера.
    Если последняя станет недоступна, вернет None.
    :param url: str - ссылка на изображение.
    :return: изображение или None.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except Exception as e:
        # print(f"Ошибка при скачивании изображения: {e}")
        pass

    try:
        response = requests.get('https://sun3-13.userapi.com/vUwuDVuR7ZBM20r76d5C1RVRG4o48C-AiD8Oeg/5lXzefLwbPs.jpg')
        response.raise_for_status()
        return response.content
    except Exception as e:
        return None


def subtract_days(days_count: int) -> datetime.date:
    """
    Вычитает необходимое количество дней из текущей даты.
    :param days_count: int - количество дней, которое нужно вычесть из текущей даты.
    :return: дата.
    """
    current_date = datetime.now()
    new_date = current_date - timedelta(days=days_count)
    return new_date
