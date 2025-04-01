import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

# Ключ телеграм-бота.
BOT_TOKEN = os.getenv('BOT_TOKEN')
# Ключ сайта, предоставляющего информацию о фильмах.
KP_API_KEY = os.getenv('CINEMA_API_KEY')
# Телеграм-идентификатор пользователя, осуществляющего очистку базы прямо из бота.
ADMIN_TG_ID = int(os.getenv('ADMIN_TG_ID'))
# Команды по умолчанию телеграм-бота. Команду service можно убрать из меню и использовать вручную.
DEFAULT_COMMANDS = (
    ('help', 'Справка'),
    ('title', 'Поиск по названию'),
    ('rating', 'Поиск по рейтингу'),
    ('history', 'История поиска'),
    ('service', 'Обслуживание БД')
)
# Полное имя БД, в которой хранится служебная информация.
DB_PATH = os.path.abspath(os.path.join(os.curdir, 'database', 'database.db'))
# Формат даты для хранения и корректного поиска в БД SQLite.
DATE_FORMAT = '%Y-%m-%d'
# Основная часть адреса сайта, предоставляющего информацию о фильмах.
SITE_BASE = 'https://api.kinopoisk.dev/'
# Список кнопок для клавиатуры, которая определяет ограничение числа возвращаемых сайтом результатов поиска.
NUM_KEYS = {1: 'key10', 2: 'key20', 3: 'key30', 4: 'key40', 5: 'key50',
            6: 'key60', 7: 'key70', 8: 'key80', 9: 'key90', 10: 'key100'}
