import datetime
import json
from loader import bot
from telebot.types import Message, CallbackQuery
from database.cinema import User, Request
from database.processing import get_film
from states.title import TitleState
from config_data.config import DATE_FORMAT, NUM_KEYS
from keyboards.inline.number import number_keys
from keyboards.inline.pagination import pagination_keys
from utils.misc import download_image
from utils.parsing import parsing_response
from api.kpdev.kp import search_movie_by_title


@bot.message_handler(state='*', commands=['title'])
def search_by_title(message: Message) -> None:
    """
    Отлавливает ввод команды поиска фильма по названию.
    Проверяет зарегистрирован ли пользователь в БД, если нет - предлагает пройти регистрацию.
    Выводит приглашение (сообщение) для ввода названия фильма.
    :param message: сообщение / команда.
    :return: None.
    """
    if User.get_or_none(User.user_id == message.from_user.id) is None:
        bot.reply_to(message, 'Вы не зарегистрированы. Выполните команду /start')
        return

    bot.send_message(message.from_user.id, 'Введите название фильма.')
    bot.set_state(message.from_user.id, TitleState.title)

    with bot.retrieve_data(message.from_user.id) as data:
        data['new_request'] = {'user_id': message.from_user.id}
        data['new_request']['date'] = datetime.date.today().strftime(DATE_FORMAT)


@bot.message_handler(state=TitleState.title)
def enter_title(message: Message) -> None:
    """
    Отлавливает ввод пользователем названия фильма.
    Выводит клавиатуру для выбора количества результатов поиска (от 10 до 100 с шагом 10).
    :param message: сообщение.
    :return: None.
    """
    with bot.retrieve_data(message.from_user.id) as data:
        data['new_request']['content'] = {'title': message.text}

    bot.send_message(message.from_user.id, 'Выберите количество результатов.', reply_markup=number_keys(NUM_KEYS))
    bot.set_state(message.from_user.id, TitleState.count)


@bot.callback_query_handler(state=TitleState.count,
                            func=lambda callback_query: (callback_query.data in NUM_KEYS.values()))
def number_keyboard_answer(callback_query: CallbackQuery) -> None:
    """
    Отслеживает выбор пользователем количества ответов при поиске фильма по названию с использованием клавиатуры.
    Получает информацию с сайта. Сохраняет в БД информацию о запросе (с ответом).
    Выводит информацию о первом фильме и клавиатуру для перелистывания ответов.
    :param callback_query: ответ клавиатуры.
    :return: None.
    """
    # bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)  # убрать клаву
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)  # убрать всё сообщение
    result = []

    with bot.retrieve_data(callback_query.from_user.id) as data:
        resp = search_movie_by_title(title=data['new_request']['content']['title'], limit=int(callback_query.data[3:]))
        result = parsing_response(response=resp)
        data['new_request']['content'] = json.dumps(data['new_request']['content'])
        data['new_request']['response'] = json.dumps(result)

    new_request = Request(**data['new_request'])
    new_request.save()

    if len(result) > 0:
        page = 1
        paginator = pagination_keys(page_count=len(result), page_current=page, data_pattern='pag_title#{page}')
        text, url = get_film(result[page - 1])
        poster = download_image(url=url)
        bot.set_state(callback_query.from_user.id, TitleState.pagination)

        if poster is not None:
            bot.send_photo(callback_query.from_user.id, photo=poster, caption=text, reply_markup=paginator)
        else:
            bot.send_message(callback_query.from_user.id, text=text, reply_markup=paginator)
    else:
        bot.delete_state(callback_query.from_user.id)
        bot.send_message(callback_query.from_user.id, 'По вашему запросу ничего не найдено.')


@bot.callback_query_handler(state=TitleState.pagination, func=lambda call: call.data.split('#')[0] == 'pag_title')
def title_pagination(callback_query: CallbackQuery) -> None:
    """
    Отлавливает нажатие пользователем кнопки на клавиатуре перелистывания
    при просмотре фильмов в режиме поиска по названию.
    :param callback_query: ответ клавиатуры.
    :return: None.
    """
    page = int(callback_query.data.split('#')[1])

    with bot.retrieve_data(callback_query.from_user.id) as data:
        result = json.loads(data['new_request']['response'])

    paginator = pagination_keys(page_count=len(result), page_current=page, data_pattern='pag_title#{page}')
    text, url = get_film(result[page - 1])
    poster = download_image(url=url)
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

    if poster is not None:
        bot.send_photo(callback_query.from_user.id, photo=poster, caption=text, reply_markup=paginator)
    else:
        bot.send_message(callback_query.from_user.id, text=text, reply_markup=paginator)


@bot.callback_query_handler(func=lambda call: call.data == 'key_back#0')
def characters_page_callback(callback_query: CallbackQuery):
    """
    Отслеживает нажатие пользователем кнопки возврата в главное меню на клавиатурах перелистывания результатов
    в разных режимах (состояниях).
    :param callback_query: ответ клавиатуры.
    :return: None.
    """
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    bot.delete_state(callback_query.from_user.id)
    bot.send_message(callback_query.message.chat.id, 'Вы вернулись в главное меню, выберите действие.')
