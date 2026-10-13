# Лабораторна робота №14. FastAPI-додаток з Ormar-моделями із зовнішніми ключами
# Виконала: Іващук Евеліна

# Тести API (фреймворк unittest). Запити надсилає TestClient - засіб FastAPI,
# який звертається до додатку напряму, без запуску сервера. Тести працюють
# з окремою тимчасовою базою даних і не змінюють файл library.db.

import os
import tempfile
import unittest

# Адресу тестової бази даних задаємо до імпорту додатку
TEST_DB = os.path.join(tempfile.mkdtemp(), "test.db").replace("\\", "/")
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///" + TEST_DB

from fastapi.testclient import TestClient

from main import app


class TestApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Запускаємо додаток один раз для всіх тестів: вхід у блок with
        # викликає події запуску (підключення до бази, створення таблиць)
        cls.context = TestClient(app)
        cls.client = cls.context.__enter__()

    @classmethod
    def tearDownClass(cls):
        # Завершуємо роботу додатку і відключаємося від бази даних
        cls.context.__exit__(None, None, None)

    def create_human(self):
        # Допоміжний метод: створює людину і повертає її номер
        data = {"name": "Olena", "surname": "Kovalenko", "age": 30}
        return self.client.post("/human/", json=data).json()["id"]

    # ---------- Хід роботи: люди і собаки ----------

    def test_human_crud(self):
        # Створення
        response = self.client.post("/human/", json={"name": "Ivan", "surname": "Bondar",
                                                     "age": 25})
        self.assertEqual(response.status_code, 201)
        human_id = response.json()["id"]
        # Читання
        self.assertEqual(self.client.get(f"/human/{human_id}").json()["name"], "Ivan")
        # Часткове оновлення: змінюємо лише вік
        response = self.client.patch(f"/human/{human_id}", json={"age": 26})
        self.assertEqual(response.json()["age"], 26)
        self.assertEqual(response.json()["surname"], "Bondar")
        # Видалення
        self.assertEqual(self.client.delete(f"/human/{human_id}").status_code, 204)
        self.assertEqual(self.client.get(f"/human/{human_id}").status_code, 404)

    def test_human_validation(self):
        # Від'ємний вік і порожнє ім'я не проходять перевірку схеми (помилка 422)
        bad_age = {"name": "Ivan", "surname": "Bondar", "age": -1}
        self.assertEqual(self.client.post("/human/", json=bad_age).status_code, 422)
        no_name = {"name": "", "surname": "Bondar", "age": 20}
        self.assertEqual(self.client.post("/human/", json=no_name).status_code, 422)

    def test_dog_with_owner(self):
        human_id = self.create_human()
        dog = {"name": "Rex", "age": 3, "is_male": True, "owner": human_id}
        response = self.client.post("/dog/", json=dog)
        self.assertEqual(response.status_code, 201)
        # У відповіді разом із собакою повертаються дані власника
        self.assertEqual(response.json()["owner"]["surname"], "Kovalenko")
        # У людини з'явилася собака (зворотний зв'язок)
        dogs = self.client.get(f"/human/{human_id}").json()["dogs"]
        self.assertEqual(dogs[0]["name"], "Rex")

    def test_dog_without_owner(self):
        dog = {"name": "Bim", "age": 1, "is_male": True}
        response = self.client.post("/dog/", json=dog)
        self.assertEqual(response.status_code, 201)
        self.assertIsNone(response.json()["owner"])

    def test_dog_with_missing_owner(self):
        # Власника з таким номером немає - собаку не створено
        dog = {"name": "Rex", "age": 3, "is_male": True, "owner": 9999}
        self.assertEqual(self.client.post("/dog/", json=dog).status_code, 404)

    def test_dog_update_owner(self):
        first = self.create_human()
        second = self.create_human()
        dog = {"name": "Lada", "age": 2, "is_male": False, "owner": first}
        dog_id = self.client.post("/dog/", json=dog).json()["id"]
        # Змінюємо власника
        response = self.client.patch(f"/dog/{dog_id}", json={"owner": second})
        self.assertEqual(response.json()["owner"]["id"], second)
        self.assertEqual(response.json()["name"], "Lada")
        # Неіснуючий власник - помилка 404, собака залишається без змін
        response = self.client.patch(f"/dog/{dog_id}", json={"owner": 9999})
        self.assertEqual(response.status_code, 404)
        # Собаку можна залишити без власника
        response = self.client.patch(f"/dog/{dog_id}", json={"owner": None})
        self.assertIsNone(response.json()["owner"])

    def test_cannot_delete_human_with_dogs(self):
        human_id = self.create_human()
        dog = {"name": "Rex", "age": 3, "is_male": True, "owner": human_id}
        dog_id = self.client.post("/dog/", json=dog).json()["id"]
        # Людину, яка має собак, видалити не можна (помилка 409)
        self.assertEqual(self.client.delete(f"/human/{human_id}").status_code, 409)
        # Після видалення собаки людину можна видалити
        self.assertEqual(self.client.delete(f"/dog/{dog_id}").status_code, 204)
        self.assertEqual(self.client.delete(f"/human/{human_id}").status_code, 204)

    def test_not_found(self):
        self.assertEqual(self.client.get("/dog/9999").status_code, 404)
        self.assertEqual(self.client.patch("/human/9999", json={"age": 1}).status_code, 404)
        self.assertEqual(self.client.delete("/dog/9999").status_code, 404)

    # ---------- Самостійне завдання: автори, книги, відгуки ----------

    def test_seed_data(self):
        # Під час запуску в базу додано початкові книги разом з авторами
        books = self.client.get("/books/").json()
        titles = [book["title"] for book in books]
        self.assertIn("1984", titles)
        book = [book for book in books if book["title"] == "1984"][0]
        self.assertEqual(book["author"]["surname"], "Orwell")

    def test_author_with_books(self):
        author = {"name": "Lesya", "surname": "Ukrainka", "birth_year": 1871}
        response = self.client.post("/authors/", json=author)
        self.assertEqual(response.status_code, 201)
        author_id = response.json()["id"]
        book = {"title": "Forest Song", "description": "Drama",
                "published_year": 1911, "author": author_id}
        response = self.client.post("/books/", json=book)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["author"]["surname"], "Ukrainka")
        book_id = response.json()["id"]
        # В автора з'явилася книга
        books = self.client.get(f"/authors/{author_id}").json()["books"]
        self.assertEqual(books[0]["title"], "Forest Song")
        # Автора, який має книги, видалити не можна
        self.assertEqual(self.client.delete(f"/authors/{author_id}").status_code, 409)
        self.assertEqual(self.client.delete(f"/books/{book_id}").status_code, 204)
        self.assertEqual(self.client.delete(f"/authors/{author_id}").status_code, 204)

    def test_book_validation(self):
        no_title = {"title": "", "published_year": 2000}
        self.assertEqual(self.client.post("/books/", json=no_title).status_code, 422)
        bad_year = {"title": "Book", "published_year": 3000}
        self.assertEqual(self.client.post("/books/", json=bad_year).status_code, 422)
        missing_author = {"title": "Book", "published_year": 2000, "author": 9999}
        self.assertEqual(self.client.post("/books/", json=missing_author).status_code, 404)

    def test_book_update(self):
        book = {"title": "Draft", "published_year": 2020}
        book_id = self.client.post("/books/", json=book).json()["id"]
        response = self.client.patch(f"/books/{book_id}", json={"title": "Final"})
        self.assertEqual(response.json()["title"], "Final")
        self.assertEqual(response.json()["published_year"], 2020)
        response = self.client.patch("/books/9999", json={"title": "X"})
        self.assertEqual(response.status_code, 404)

    def test_reviews(self):
        book = {"title": "Reviewed book", "published_year": 2021}
        book_id = self.client.post("/books/", json=book).json()["id"]
        review = {"reviewer": "Maria", "rating": 5, "text": "Great!", "book": book_id}
        response = self.client.post("/reviews/", json=review)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["book"]["title"], "Reviewed book")
        review_id = response.json()["id"]
        # Оцінка має бути від 1 до 5
        bad = {"reviewer": "Maria", "rating": 6, "book": book_id}
        self.assertEqual(self.client.post("/reviews/", json=bad).status_code, 422)
        # Відгук про неіснуючу книгу створити не можна
        missing = {"reviewer": "Maria", "rating": 4, "book": 9999}
        self.assertEqual(self.client.post("/reviews/", json=missing).status_code, 404)
        # Оновлення оцінки
        response = self.client.patch(f"/reviews/{review_id}", json={"rating": 3})
        self.assertEqual(response.json()["rating"], 3)
        # Відгук не можна залишити без книги
        response = self.client.patch(f"/reviews/{review_id}", json={"book": None})
        self.assertEqual(response.status_code, 422)
        # Список відгуків про книгу
        reviews = self.client.get(f"/books/{book_id}/reviews").json()
        self.assertEqual(len(reviews), 1)
        # Разом з книгою видаляються її відгуки (каскадне видалення)
        self.assertEqual(self.client.delete(f"/books/{book_id}").status_code, 204)
        self.assertEqual(self.client.get(f"/reviews/{review_id}").status_code, 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)
