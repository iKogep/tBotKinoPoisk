from telebot.types import Message
from loader import bot
from config_data.config import DEFAULT_COMMANDS


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message) -> None:
    """ Отлавливает сообщения пользователя без состояния. Выводит список доступных команд. """
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, '\n'.join(text))
