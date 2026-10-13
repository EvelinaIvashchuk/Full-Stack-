# Лабораторна робота №14. FastAPI-додаток з Ormar-моделями із зовнішніми ключами
# Виконала: Іващук Евеліна

# Модуль schemas містить схеми Pydantic. Схема описує, які дані користувач
# може надіслати в запиті, і перевіряє їх ще до звернення до бази даних.
# Create-схеми використовуються для створення записів, Update-схеми - для
# часткового оновлення (метод PATCH): у них усі поля необов'язкові.

from typing import Optional

from pydantic import BaseModel, Field


# ---------- Схеми з ходу роботи ----------

class HumanCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    surname: str = Field(min_length=1, max_length=50)
    age: int = Field(ge=0)    # ge=0: значення має бути не менше 0


class HumanUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    surname: Optional[str] = Field(None, min_length=1, max_length=50)
    age: Optional[int] = Field(None, ge=0)


class DogCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    age: int = Field(ge=0)
    is_male: bool
    owner: Optional[int] = None    # номер власника або None, якщо власника немає


class DogUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    age: Optional[int] = Field(None, ge=0)
    is_male: Optional[bool] = None
    owner: Optional[int] = None


# ---------- Схеми самостійного завдання ----------

class AuthorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    surname: str = Field(min_length=1, max_length=50)
    birth_year: Optional[int] = Field(None, ge=0, le=2100)


class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    surname: Optional[str] = Field(None, min_length=1, max_length=50)
    birth_year: Optional[int] = Field(None, ge=0, le=2100)


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = ""
    published_year: int = Field(ge=0, le=2100)
    author: Optional[int] = None    # номер автора або None


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    published_year: Optional[int] = Field(None, ge=0, le=2100)
    author: Optional[int] = None


class ReviewCreate(BaseModel):
    reviewer: str = Field(min_length=1, max_length=50)
    rating: int = Field(ge=1, le=5)    # оцінка від 1 до 5
    text: str = ""
    book: int                          # номер книги, обов'язковий


class ReviewUpdate(BaseModel):
    reviewer: Optional[str] = Field(None, min_length=1, max_length=50)
    rating: Optional[int] = Field(None, ge=1, le=5)
    text: Optional[str] = None
    book: Optional[int] = None
