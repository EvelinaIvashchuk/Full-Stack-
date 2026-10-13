# Лабораторна робота №14. FastAPI-додаток з Ormar-моделями із зовнішніми ключами
# Виконала: Іващук Евеліна

# Модуль models містить Ormar-моделі. Кожна модель - це таблиця бази даних.
# Зовнішній ключ (ForeignKey) пов'язує запис однієї таблиці із записом іншої.

from typing import Optional

import ormar

from database import base_ormar_config


# ---------- Моделі з ходу роботи: людина і собака ----------

class Human(ormar.Model):
    # Налаштування моделі: спільні параметри і назва таблиці
    ormar_config = base_ormar_config.copy(tablename="human")

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=50)
    surname: str = ormar.String(max_length=50)
    age: int = ormar.Integer(minimum=0)


class Dog(ormar.Model):
    ormar_config = base_ormar_config.copy(tablename="dog")

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=50)
    age: int = ormar.Integer(minimum=0)
    is_male: bool = ormar.Boolean()

    # Зовнішній ключ: власник собаки - запис із таблиці human.
    # nullable=True означає, що собака може не мати власника.
    # У моделі Human автоматично з'являється зворотний зв'язок dogs.
    owner: Optional[Human] = ormar.ForeignKey(Human, nullable=True, related_name="dogs")


# ---------- Моделі самостійного завдання: автор, книга, відгук ----------

class Author(ormar.Model):
    ormar_config = base_ormar_config.copy(tablename="authors")

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=50)
    surname: str = ormar.String(max_length=50)
    birth_year: Optional[int] = ormar.Integer(nullable=True)


class Book(ormar.Model):
    # Модель книги з попередньої лабораторної роботи, до якої додано автора
    ormar_config = base_ormar_config.copy(tablename="books")

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=100)
    description: str = ormar.Text()
    published_year: int = ormar.Integer()

    # Зовнішній ключ на автора: один автор може мати багато книг.
    # Автора, в якого є книги, видалити не можна.
    author: Optional[Author] = ormar.ForeignKey(Author, nullable=True, related_name="books")


class Review(ormar.Model):
    ormar_config = base_ormar_config.copy(tablename="reviews")

    id: int = ormar.Integer(primary_key=True)
    reviewer: str = ormar.String(max_length=50)
    rating: int = ormar.Integer(minimum=1, maximum=5)
    text: str = ormar.Text()

    # Зовнішній ключ на книгу: відгук не існує без книги (nullable=False).
    # ondelete="CASCADE" означає, що разом з книгою видаляються і її відгуки.
    book: Book = ormar.ForeignKey(Book, nullable=False, ondelete="CASCADE",
                                  related_name="reviews")
