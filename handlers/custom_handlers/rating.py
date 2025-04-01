import datetime
import json
from loader import bot
from telebot.types import Message, CallbackQuery
from database.cinema import User, Request
from database.processing import get_film
from states.rating import RatingState
from config_data.config import DATE_FORMAT, NUM_KEYS
from keyboards.inline.genre import genre_keys
from keyboards.inline.number import number_keys
from keyboards.inline.pagination import pagination_keys
from api.kpdev.kp import get_genre, search_movie_by_rating
from utils.check import checking_rating_format
from utils.misc import download_image
from utils.parsing import parsing_response


GENRE_LIST = get_genre()


@bot.message_handler(state='*', commands=['rating'])
def search_by_rating(message: Message) -> None:
    """
    Отслеживает ввод пользователем команды поиска фильма по рейтингу.
    Проверяет зарегистрирован ли пользователь в БД, если нет - предлагает осуществить регистрацию.
    Выводит клавиатуру со списком жанров.
    :param message:
    :return:
    """
    if User.get_or_none(User.user_id == message.from_user.id) is None:
        bot.reply_to(message, 'Вы не зарегистрированы. Выполните команду /start')
        return

    bot.send_message(message.from_user.id, 'Выберите жанр.', reply_markup=genre_keys(GENRE_LIST))
    bot.set_state(message.from_user.id, RatingState.genre)

    with bot.retrieve_data(message.from_user.id) as data:
        data['new_request'] = {'user_id': message.from_user.id}
        data['new_request']['date'] = datetime.date.today().strftime(DATE_FORMAT)


@bot.callback_query_handler(state=RatingState.genre,
                            func=lambda callback_query: (callback_query.data in GENRE_LIST))
def genre_keyboard_answer(callback_query: CallbackQuery) -> None:
    """
    Отслеживает выбор пользователем жанра с использованием клавиатуры.
    Выводит приглашение к вводу рейтинга (диапазона) фильма.
    :param callback_query: ответ клавиатуры.
    :return: None.
    """
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    bot.send_message(callback_query.from_user.id,
                     'Введите рейтинг в формате числа от 1 до 10 или диапазона вида: "8-10" (без кавычек).')

    with bot.retrieve_data(callback_query.from_user.id) as data:
        data['new_request']['content'] = {'genre': str(callback_query.data)}

    bot.set_state(callback_query.from_user.id, RatingState.rating)


@bot.message_handler(state=RatingState.rating)
def enter_rating(message: Message) -> None:
    """
    Отслеживает ввод пользователем рейтинга (диапазона) фильма.
    Выводит клавиатуру для выбора количества результатов поиска.
    :param message: сообщение.
    :return: None.
    """
    if checking_rating_format(message.text):
        with bot.retrieve_data(message.from_user.id) as data:
            data['new_request']['content']['rating'] = message.text

        bot.send_message(message.from_user.id, 'Выберите количество результатов.', reply_markup=number_keys(NUM_KEYS))
        bot.set_state(message.from_user.id, RatingState.count)
    else:
        text = 'Неверный формат рейтинга.\n' \
               'Рейтинг это целое число от 1 до 10.\n' \
               'Можно указать диапазон в формате: целое число (меньшее), дефис, целое число (большее), например:\n' \
               '8-10'
        bot.send_message(message.from_user.id, text)


@bot.callback_query_handler(state=RatingState.count,
                            func=lambda callback_query: (callback_query.data in NUM_KEYS.values()))
def number_keyboard_answer(callback_query: CallbackQuery) -> None:
    """
    Отслеживает выбор пользователем количества ответов с использованием клавиатуры в режиме поиска фильмов по рейтингу.
    Сохраняет в БД информацию о запросе (с ответом).
    Выводит информацию о первом фильме и клавиатуру для перелистывания ответов.
    :param callback_query: ответ клавиатуры.
    :return: None.
    """
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    result = []

    with bot.retrieve_data(callback_query.from_user.id) as data:
        resp = search_movie_by_rating(genre=data['new_request']['content']['genre'],
                                      rating=data['new_request']['content']['rating'],
                                      limit=int(callback_query.data[3:]))
        result = parsing_response(resp)
        data['new_request']['content'] = json.dumps(data['new_request']['content'])
        data['new_request']['response'] = json.dumps(result)

    new_request = Request(**data['new_request'])
    new_request.save()

    if len(result) > 0:
        page = 1
        paginator = pagination_keys(page_count=len(result), page_current=page, data_pattern='pag_rating#{page}')
        text, url = get_film(result[page - 1])
        poster = download_image(url=url)
        bot.set_state(callback_query.from_user.id, RatingState.pagination)

        if poster is not None:
            bot.send_photo(callback_query.from_user.id, photo=poster, caption=text, reply_markup=paginator)
        else:
            bot.send_message(callback_query.from_user.id, text=text, reply_markup=paginator)
    else:
        bot.delete_state(callback_query.from_user.id)
        bot.send_message(callback_query.from_user.id, 'По вашему запросу ничего не найдено.')


@bot.callback_query_handler(state=RatingState.pagination, func=lambda call: call.data.split('#')[0] == 'pag_rating')
def rating_pagination(callback_query: CallbackQuery) -> None:
    """
    Отслеживает нажатие пользователем кнопок перелистывания в режиме поиска фильмов по рейтингу.
    Удаляет предыдущее сообщение. Выводит соответствующий фильм и клавиатуру перелистывания.
    :param callback_query: ответ клавиатуры.
    :return: None.
    """
    page = int(callback_query.data.split('#')[1])

    with bot.retrieve_data(callback_query.from_user.id) as data:
        result = json.loads(data['new_request']['response'])

    paginator = pagination_keys(page_count=len(result), page_current=page, data_pattern='pag_rating#{page}')
    text, url = get_film(result[page - 1])
    poster = download_image(url=url)
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

    if poster is not None:
        bot.send_photo(callback_query.from_user.id, photo=poster, caption=text, reply_markup=paginator)
    else:
        bot.send_message(callback_query.from_user.id, text=text, reply_markup=paginator)
