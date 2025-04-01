import datetime
from loader import bot
from telebot.types import Message, CallbackQuery
from config_data.config import DATE_FORMAT
from states.other import OtherState
from database.cinema import User
from database.processing import get_history, get_film
from keyboards.inline.history import date_key, history_key
from keyboards.inline.pagination import pagination_keys
from utils.misc import download_image


@bot.message_handler(state='*', commands=['history'])
def history_choice(message: Message) -> None:
    """
    Отлавливает выбор пользователем команды просмотра истории запросов.
    Проверяет, зарегистрирован ли пользователь в БД, если нет, то предлагает сначала зарегистрироваться.
    Выводит сообщение и клавиатуру с вариантами дат и диапазонов просмотра истории.
    :param message: сообщение / команда.
    :return: None.
    """
    if User.get_or_none(User.user_id == message.from_user.id) is None:
        bot.reply_to(message, 'Вы не зарегистрированы. Выполните команду /start')
        return

    text = 'История запросов хранится не более 30 дней.\n' \
           'Для просмотра истории выберите диапазон.\n' \
           'Будет выведено не более 99 поисковых запросов.'
    bot.send_message(message.from_user.id, text, reply_markup=date_key())
    bot.set_state(message.from_user.id, OtherState.history_search)

    with bot.retrieve_data(message.from_user.id) as data:
        data['new_request'] = {'user_id': message.from_user.id}  # todo correct HAX
        data['new_request']['date'] = datetime.date.today().strftime(DATE_FORMAT)  # todo correct HAX


@bot.callback_query_handler(state=OtherState.history_search, func=lambda call: call.data.split('#')[0] == 'date')
def history_date(callback_query: CallbackQuery) -> None:
    """
    Отслеживает выбор диапазона просмотра истории запросов с помощью клавиатуры.
    Запрашивает из БД информацию об истории запросов, выводит пользователю список запросов в виде текста
    и клавиатуру с соответствующим количеством кнопок, для выбора нужного запроса.
    :param callback_query: ответ клавиатуры.
    :return: None.
    """
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    history_text, history_dict = get_history(user_id=callback_query.from_user.id, dt=callback_query.data.split('#')[1])

    with bot.retrieve_data(callback_query.from_user.id) as data:
        data['new_request']['content'] = history_text
        data['new_request']['response'] = history_dict

    bot.send_message(callback_query.from_user.id, history_text, reply_markup=history_key(len(history_dict.keys())))
    bot.set_state(callback_query.from_user.id, OtherState.history_view)


@bot.callback_query_handler(state=OtherState.history_view, func=lambda call: call.data.split('#')[0] == 'hist')
def history_view(callback_query: CallbackQuery) -> None:
    """
    Отслеживает выбор пользователем номера запроса из списка с помощью клавиатуры.
    Выводит информацию о первом фильме из списка результатов (новый запрос к сайту не осуществляется)
    и выводит клавиатуру для пролистывания фильмов.
    :param callback_query: ответ клавиатуры.
    :return: None.
    """
    history_number = int(callback_query.data.split('#')[1])
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

    with bot.retrieve_data(callback_query.from_user.id) as data:
        result = data['new_request']['response'][history_number]
        data['new_request']['result'] = result

    if len(result) > 0:
        page = 1
        paginator = pagination_keys(page_count=len(result), page_current=page,
                                    data_pattern='pag_hist#{page}', back_key=1)
        text, url = get_film(result[page - 1])
        poster = download_image(url=url)
        bot.set_state(callback_query.from_user.id, OtherState.history_page)

        if poster is not None:
            bot.send_photo(callback_query.from_user.id, photo=poster, caption=text, reply_markup=paginator)
        else:
            bot.send_message(callback_query.from_user.id, text=text, reply_markup=paginator)
    else:
        bot.delete_state(callback_query.from_user.id)
        bot.send_message(callback_query.from_user.id, 'По выбранному запросу не было результата.')


@bot.callback_query_handler(state=OtherState.history_page, func=lambda call: call.data.split('#')[0] == 'pag_hist')
def title_pagination(callback_query: CallbackQuery) -> None:
    """
    Отлавливает нажатие клавиатуры при пролистывании фильмов из истории запроса.
    Удаляет старое сообщение и выводит новое, в соответствии с выбором пользователя.
    :param callback_query: ответ клавиатуры.
    :return: None.
    """
    page = int(callback_query.data.split('#')[1])

    with bot.retrieve_data(callback_query.from_user.id) as data:
        result = data['new_request']['result']

    paginator = pagination_keys(page_count=len(result), page_current=page, data_pattern='pag_hist#{page}', back_key=1)
    text, url = get_film(result[page - 1])
    poster = download_image(url=url)
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

    if poster is not None:
        bot.send_photo(callback_query.from_user.id, photo=poster, caption=text, reply_markup=paginator)
    else:
        bot.send_message(callback_query.from_user.id, text=text, reply_markup=paginator)


@bot.callback_query_handler(func=lambda call: call.data == 'key_back#1')
def characters_page_callback(callback_query: CallbackQuery):
    """
    Отлавливает нажатие кнопки возврата на клавиатуре пролистывания фильмов из истории запросов.
    Повторно выводит список запросов за указанную ранее дату (период),
    что бы пользователь смог просмотреть детали другого запроса.
    :param callback_query: ответ клавиатуры.
    :return: None.
    """
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

    with bot.retrieve_data(callback_query.from_user.id) as data:
        history_text = data['new_request']['content']
        history_dict = data['new_request']['response']

    bot.send_message(callback_query.from_user.id, history_text, reply_markup=history_key(len(history_dict.keys())))
    bot.set_state(callback_query.from_user.id, OtherState.history_view)
