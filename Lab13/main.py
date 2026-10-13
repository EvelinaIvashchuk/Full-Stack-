# Лабораторна робота №13. FastAPI-додаток з Ormar-моделлю та PostgreSQL
# Виконала: Іващук Евеліна

# FastAPI-додаток "Books API": модель Book (бібліотека Ormar, без зовнішніх
# ключів) зберігається в базі даних PostgreSQL. Додаток і база даних
# запускаються в контейнерах Docker.

import os    # читання змінних середовища

import databases       # асинхронна робота з базою даних
import nest_asyncio    # дозволяє вкладені цикли подій asyncio
import ormar           # ORM: опис таблиць бази даних у вигляді класів
import sqlalchemy      # створення таблиць у базі даних
from fastapi import FastAPI, HTTPException
from ormar.exceptions import NoMatch    # виняток "запис не знайдено"

# ---------- Підключення до бази даних ----------

# Адреса підключення до PostgreSQL. У контейнері вона береться зі змінної
# середовища DATABASE_URL (її задано у файлі docker-compose.yml), а значення
# за замовчуванням використовується для запуску без Docker.
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://user:password@localhost:5432/booksdb"
)

database = databases.Database(DATABASE_URL)       # об'єкт для асинхронних запитів
metadata = sqlalchemy.MetaData()                  # опис усіх таблиць
engine = sqlalchemy.create_engine(DATABASE_URL)   # з'єднання для створення таблиць


# ---------- Модель даних ----------

class Book(ormar.Model):
    # Модель описує таблицю books: її поля і типи даних у них

    class Meta:
        # Службовий клас, який пов'язує модель з базою даних
        tablename = "books"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)        # унікальний номер (первинний ключ)
    title: str = ormar.String(max_length=100)        # назва книги, до 100 символів
    description: str = ormar.Text()                  # короткий опис
    published_year: int = ormar.Integer()            # рік видання


# ---------- Ініціалізація FastAPI-додатку ----------

app = FastAPI(title="Books API")
nest_asyncio.apply()


# ---------- Початкові дані ----------

async def seed_data():
    # Функція додає в таблицю три книги, якщо таблиця порожня.
    # Слово async означає, що функція асинхронна, а await - що програма
    # чекає на відповідь бази даних, не блокуючи обробку інших запитів.
    if await Book.objects.count() == 0:
        books_data = [
            {"title": "1984", "description": "Dystopian novel",
             "published_year": 1949},
            {"title": "To Kill a Mockingbird", "description": "Classic novel",
             "published_year": 1960},
            {"title": "The Great Gatsby", "description": "Novel by F. Scott Fitzgerald",
             "published_year": 1925},
        ]
        for book in books_data:
            # **book передає елементи словника як іменовані аргументи
            await Book.objects.create(**book)
        print("Initial data is added to the database")


# ---------- Події запуску та завершення ----------

@app.on_event("startup")
async def startup():
    # Під час запуску додатку створюємо таблиці (якщо їх ще немає),
    # підключаємося до бази даних і додаємо початкові дані
    metadata.create_all(engine)
    if not database.is_connected:
        await database.connect()
    await seed_data()


@app.on_event("shutdown")
async def shutdown():
    # Під час завершення роботи розриваємо підключення до бази даних
    if database.is_connected:
        await database.disconnect()


# ---------- API-ендпоїнти ----------

@app.get("/books/", tags=["Books"])
async def get_all_books():
    # Повертає список усіх книг
    return await Book.objects.all()


@app.get("/books/{book_id}", tags=["Books"])
async def get_book_by_id(book_id: int):
    # Повертає книгу з номером book_id. Якщо такої книги немає,
    # повертає помилку 404.
    try:
        book = await Book.objects.get(id=book_id)
        return book
    except NoMatch:
        raise HTTPException(status_code=404, detail="Book not found")
