import os.path
from telebot.custom_filters import StateFilter
from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands
from database.cinema import create_models
from config_data.config import DB_PATH


if __name__ == "__main__":
    # Проверяем наличие файла БД, при необходимости создаем новый.
    if not os.path.exists(DB_PATH):
        create_models()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()
