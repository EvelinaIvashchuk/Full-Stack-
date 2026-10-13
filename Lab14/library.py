# Лабораторна робота №14. FastAPI-додаток з Ormar-моделями із зовнішніми ключами
# Виконала: Іващук Евеліна

# Модуль library - самостійне завдання: CRUD-операції (створення, читання,
# оновлення, видалення) для моделей Author, Book і Review.
# Ендпоїнти зібрано в об'єкті APIRouter, який підключається до додатку в main.py.

from fastapi import APIRouter, HTTPException, Response
from ormar.exceptions import NoMatch
from sqlalchemy.exc import IntegrityError    # порушення цілісності бази даних

from models import Author, Book, Review
from schemas import (AuthorCreate, AuthorUpdate, BookCreate, BookUpdate,
                     ReviewCreate, ReviewUpdate)

router = APIRouter()


# ---------- Допоміжні функції ----------

async def get_author_or_404(author_id: int):
    # Повертає автора або помилку 404, якщо автора з таким номером немає
    try:
        return await Author.objects.get(id=author_id)
    except NoMatch:
        raise HTTPException(status_code=404,
                            detail=f"Author with id {author_id} not found!")


async def get_book_or_404(book_id: int):
    # select_related("author") завантажує разом з книгою дані її автора
    try:
        return await Book.objects.select_related("author").get(id=book_id)
    except NoMatch:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found!")


async def get_review_or_404(review_id: int):
    try:
        return await Review.objects.select_related("book").get(id=review_id)
    except NoMatch:
        raise HTTPException(status_code=404,
                            detail=f"Review with id {review_id} not found!")


async def seed_data():
    # Додає початкові дані, якщо таблиця книг порожня
    if await Book.objects.count() == 0:
        orwell = await Author(name="George", surname="Orwell", birth_year=1903).save()
        lee = await Author(name="Harper", surname="Lee", birth_year=1926).save()
        await Book(title="1984", description="Dystopian novel",
                   published_year=1949, author=orwell).save()
        await Book(title="Animal Farm", description="Satirical novella",
                   published_year=1945, author=orwell).save()
        await Book(title="To Kill a Mockingbird", description="Classic novel",
                   published_year=1960, author=lee).save()


# ---------- Автори ----------

@router.get("/authors/", tags=["Authors"])
async def get_authors():
    return await Author.objects.all()


@router.get("/authors/{id}", tags=["Authors"])
async def get_author_by_id(id: int):
    # Разом з автором повертаємо список його книг (зворотний зв'язок books)
    try:
        return await Author.objects.select_related("books").get(id=id)
    except NoMatch:
        raise HTTPException(status_code=404, detail=f"Author with id {id} not found!")


@router.post("/authors/", tags=["Authors"], status_code=201)
async def create_author(author: AuthorCreate):
    # model_dump() перетворює схему на словник, ** передає його як аргументи
    return await Author(**author.model_dump()).save()


@router.patch("/authors/{id}", tags=["Authors"])
async def update_author(id: int, author: AuthorUpdate):
    db_author = await get_author_or_404(id)
    # exclude_unset=True залишає лише ті поля, які користувач надіслав у запиті
    await db_author.update(**author.model_dump(exclude_unset=True))
    return db_author


@router.delete("/authors/{id}", tags=["Authors"])
async def delete_author(id: int):
    db_author = await get_author_or_404(id)
    try:
        await db_author.delete()
    except IntegrityError:
        # База даних не дозволяє видалити автора, на якого посилаються книги
        raise HTTPException(status_code=409,
                            detail=f"Author with id {id} has books and cannot be deleted!")
    return Response(status_code=204)


# ---------- Книги ----------

@router.get("/books/", tags=["Books"])
async def get_books():
    return await Book.objects.select_related("author").all()


@router.get("/books/{id}", tags=["Books"])
async def get_book_by_id(id: int):
    return await get_book_or_404(id)


@router.post("/books/", tags=["Books"], status_code=201)
async def create_book(book: BookCreate):
    # Перевіряємо цілісність даних: якщо автора вказано, він має існувати
    if book.author is not None:
        await get_author_or_404(book.author)
    new_book = await Book(**book.model_dump()).save()
    return await get_book_or_404(new_book.id)


@router.patch("/books/{id}", tags=["Books"])
async def update_book(id: int, book: BookUpdate):
    db_book = await get_book_or_404(id)
    data = book.model_dump(exclude_unset=True)
    if data.get("author") is not None:
        await get_author_or_404(data["author"])
    await db_book.update(**data)
    return await get_book_or_404(id)


@router.delete("/books/{id}", tags=["Books"])
async def delete_book(id: int):
    db_book = await get_book_or_404(id)
    # Відгуки про книгу видаляються автоматично (ondelete="CASCADE" у моделі)
    await db_book.delete()
    return Response(status_code=204)


# ---------- Відгуки ----------

@router.get("/reviews/", tags=["Reviews"])
async def get_reviews():
    return await Review.objects.select_related("book").all()


@router.get("/reviews/{id}", tags=["Reviews"])
async def get_review_by_id(id: int):
    return await get_review_or_404(id)


@router.get("/books/{id}/reviews", tags=["Reviews"])
async def get_reviews_of_book(id: int):
    # Усі відгуки про одну книгу: фільтруємо за зовнішнім ключем
    await get_book_or_404(id)
    return await Review.objects.filter(book=id).all()


@router.post("/reviews/", tags=["Reviews"], status_code=201)
async def create_review(review: ReviewCreate):
    # Книга, до якої додається відгук, має існувати
    await get_book_or_404(review.book)
    new_review = await Review(**review.model_dump()).save()
    return await get_review_or_404(new_review.id)


@router.patch("/reviews/{id}", tags=["Reviews"])
async def update_review(id: int, review: ReviewUpdate):
    db_review = await get_review_or_404(id)
    data = review.model_dump(exclude_unset=True)
    if "book" in data:
        # Відгук не може залишитися без книги
        if data["book"] is None:
            raise HTTPException(status_code=422, detail="A review must have a book!")
        await get_book_or_404(data["book"])
    await db_review.update(**data)
    return await get_review_or_404(id)


@router.delete("/reviews/{id}", tags=["Reviews"])
async def delete_review(id: int):
    db_review = await get_review_or_404(id)
    await db_review.delete()
    return Response(status_code=204)
