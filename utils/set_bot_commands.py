import telebot
from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot: telebot.TeleBot) -> None:
    """
    Устанавливает боту список команд по умолчанию.
    :param bot: экземпляр телеграм бота.
    :return: None.
    """
    bot.set_my_commands([BotCommand(*i) for i in DEFAULT_COMMANDS])
