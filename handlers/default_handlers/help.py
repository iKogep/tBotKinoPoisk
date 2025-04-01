from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot


# Этот хэндлер ловит команду help
@bot.message_handler(commands=['help'])
def bot_help(message: Message) -> None:
    """ Команда по-умолчанию. Справка. Выводит список доступных команд. """
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, '\n'.join(text))
