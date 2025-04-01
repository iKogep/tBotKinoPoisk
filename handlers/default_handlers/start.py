from telebot.types import Message
from peewee import IntegrityError
from loader import bot
from database.cinema import User


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """ Команда по-умолчанию. Старт. Добавляет пользователя в БД. """
    # Получаем данные пользователя.
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    try:
        # Без создания экземпляра класса, производим запись в базу.
        # Так как поле user_id является уникальным, то при попытке добавить существующего пользователя получим ошибку.
        # Возникновение ошибки в данном случае свидетельствует о наличии пользователя в базе.
        User.create(user_id=user_id, username=username, first_name=first_name, last_name=last_name)
        start_text = 'Добро пожаловать!\n' \
                     'Данный бот позволяет осуществить поиск информации о фильме.\n' \
                     'Для выбора действия нажмите кнопку меню.'
        bot.reply_to(message, start_text)
    except IntegrityError:
        bot.reply_to(message, f'Рад вас снова видеть, {first_name}!')
