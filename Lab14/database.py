# Лабораторна робота №14. FastAPI-додаток з Ormar-моделями із зовнішніми ключами
# Виконала: Іващук Евеліна

# Модуль database містить підключення до бази даних, спільне для всіх моделей.

import os    # читання змінних середовища і робота зі шляхами

import ormar         # ORM: опис таблиць бази даних у вигляді класів
import sqlalchemy    # опис структури таблиць

# За замовчуванням використовується база даних SQLite у файлі library.db
# поруч з програмою. Іншу базу даних (наприклад, PostgreSQL) можна підключити,
# задавши її адресу у змінній середовища DATABASE_URL.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(BASE_DIR, "library.db").replace("\\", "/")
DEFAULT_URL = "sqlite+aiosqlite:///" + DATABASE_FILE
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_URL)

# Об'єкт для асинхронної роботи з базою даних
database = ormar.DatabaseConnection(DATABASE_URL)

# Об'єкт, у якому зберігається опис усіх таблиць
metadata = sqlalchemy.MetaData()

# Спільні налаштування моделей: кожна модель копіює їх і додає назву своєї таблиці
base_ormar_config = ormar.OrmarConfig(metadata=metadata, database=database)
