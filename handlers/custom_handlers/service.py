from loader import bot
from telebot.types import Message, CallbackQuery
from config_data.config import ADMIN_TG_ID
from states.other import OtherState
from database.cinema import User
from database.processing import get_stat_info, clear_base
from keyboards.inline.service import service_key


@bot.message_handler(state='*', commands=['service'])
def history_choice(message: Message) -> None:
    """
    Отслеживает ввод пользователем команды обслуживания БД.
    Проверяет зарегистрирован ли пользователь в БД, если нет - предлагает пройти регистрацию.
    Проверяет, является ли пользователь администратором БД, если нет - выдает отказ.
    Возвращает клавиатуру сервисных операций.
    :param message: сообщение / команда.
    :return: None.
    """
    if User.get_or_none(User.user_id == message.from_user.id) is None:
        bot.reply_to(message, 'Вы не зарегистрированы. Выполните команду /start')
        return

    if message.from_user.id != ADMIN_TG_ID:
        bot.reply_to(message, 'Вам недоступна данная операция, так как Вы не являетесь администратором бота.')
        return

    text = get_stat_info()
    bot.send_message(message.from_user.id, text, reply_markup=service_key())
    bot.set_state(message.from_user.id, OtherState.service_clean)


@bot.callback_query_handler(state=OtherState.service_clean, func=lambda call: call.data.split('#')[0] == 'service')
def service_clear_base(callback_query: CallbackQuery) -> None:
    """
    Отслеживает нажатие пользователем кнопки очистки старых данных в БД.
    Выводит сообщение с результатом операции.
    :param callback_query: ответ клавиатуры.
    :return: None.
    """
    operation = int(callback_query.data.split('#')[1])
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    bot.delete_state(callback_query.from_user.id)
    if operation == 0:
        result = clear_base()
        bot.send_message(callback_query.from_user.id, result)
