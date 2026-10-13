# Лабораторна робота №10. Робота з Flask
# Виконала: Іващук Евеліна

# Сайт музичного гурту "Океан Ельзи" на веб-фреймворку Flask.
# Сторінки: "Головна", "Про проект", "Історія гурту" і сторінки альбомів.
# Авторизовані користувачі можуть додавати, редагувати і видаляти альбоми.

import os         # робота зі шляхами та змінними середовища
import sqlite3    # вбудована база даних SQLite
from functools import wraps    # зберігає назву функції, обгорнутої декоратором

from flask import (Flask, abort, flash, g, redirect, render_template,
                   request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

# Файл бази даних лежить у тій самій папці, що й програма
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "band.db")

# Створюємо застосунок Flask
app = Flask(__name__)

# Секретний ключ потрібен для підпису даних сесії (cookie користувача).
# На сервері він береться зі змінної середовища SECRET_KEY,
# а значення за замовчуванням використовується лише для локального запуску.
app.secret_key = os.environ.get("SECRET_KEY", "local-development-key")


# ---------- Робота з базою даних ----------

def get_db():
    # Функція повертає з'єднання з базою даних для поточного запиту.
    # Об'єкт g існує протягом одного запиту, тому з'єднання створюється один раз.
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        # Row дозволяє звертатися до полів рядка за назвою: album["title"]
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    # Після завершення запиту закриваємо з'єднання з базою даних
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    # Функція створює таблиці, якщо їх ще немає, і додає початкові альбоми
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS albums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            description TEXT NOT NULL,
            tracks TEXT NOT NULL
        )
    """)

    # Якщо таблиця альбомів порожня, заповнюємо її початковими даними
    count = db.execute("SELECT COUNT(*) FROM albums").fetchone()[0]
    if count == 0:
        albums = [
            ("Там, де нас нема", 1998,
             "The debut studio album, released after the band moved from Lviv to Kyiv.",
             "Там, де нас нема\nНовий день"),
            ("Модель", 2001,
             "The third studio album of the band.",
             "Друг\n911\nВставай"),
            ("Суперсиметрія", 2003,
             "The fourth studio album, followed by a large tour across Ukraine.",
             "Кішка\nМайже весна\nХолодно\nДівчина"),
            ("GLORIA", 2005,
             "The fifth studio album, recorded with a renewed line-up.",
             "Без бою\nВище неба\nНе питай"),
            ("Земля", 2013,
             "The eighth studio album of the band.",
             "Обійми\nСтріляй\nRendez-vous\nЯ їду додому"),
        ]
        # Знаки ? - це місця для значень: бібліотека сама безпечно підставляє
        # їх у запит, що захищає від SQL-ін'єкцій
        db.executemany(
            "INSERT INTO albums (title, year, description, tracks) VALUES (?, ?, ?, ?)",
            albums,
        )
    db.commit()


# ---------- Авторизація ----------

def login_required(view):
    # Декоратор для сторінок, доступних лише авторизованим користувачам.
    # Якщо користувач не увійшов, його перенаправляє на сторінку входу.
    @wraps(view)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to manage albums.")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapper


@app.context_processor
def inject_albums():
    # Функція передає список альбомів у всі шаблони,
    # щоб посилання на сторінки альбомів були в меню кожної сторінки
    albums = get_db().execute("SELECT id, title, year FROM albums ORDER BY year").fetchall()
    return {"menu_albums": albums}


@app.route("/register", methods=["GET", "POST"])
def register():
    # Сторінка реєстрації: GET показує форму, POST обробляє надіслані дані
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        db = get_db()

        if len(username) < 3:
            flash("The username must contain at least 3 characters.")
        elif len(password) < 6:
            flash("The password must contain at least 6 characters.")
        elif db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone():
            flash("This username is already taken.")
        else:
            # У базі зберігаємо не сам пароль, а його хеш
            db.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
            flash("Registration completed. Now you can log in.")
            return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Сторінка входу
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        user = get_db().execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        # Перевіряємо, що користувач існує і що пароль відповідає збереженому хешу
        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Incorrect username or password.")
        else:
            # Запам'ятовуємо користувача в сесії
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("You are logged in.")
            return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    # Вихід: очищаємо сесію
    session.clear()
    flash("You are logged out.")
    return redirect(url_for("index"))


# ---------- Основні сторінки ----------

@app.route("/")
def index():
    # Головна сторінка зі списком альбомів
    albums = get_db().execute("SELECT * FROM albums ORDER BY year").fetchall()
    return render_template("index.html", albums=albums)


@app.route("/about")
def about():
    # Сторінка "Про проект"
    return render_template("about.html")


@app.route("/history")
def history():
    # Сторінка "Історія гурту"
    return render_template("history.html")


# ---------- Альбоми ----------

def get_album(album_id):
    # Функція повертає альбом за його номером або показує сторінку 404
    album = get_db().execute("SELECT * FROM albums WHERE id = ?", (album_id,)).fetchone()
    if album is None:
        abort(404)
    return album


def read_album_form():
    # Функція читає і перевіряє дані форми альбому.
    # Повертає словник з даними і список повідомлень про помилки.
    data = {
        "title": request.form["title"].strip(),
        "year": request.form["year"].strip(),
        "description": request.form["description"].strip(),
        "tracks": request.form["tracks"].strip(),
    }
    errors = []
    if data["title"] == "":
        errors.append("The title is required.")
    if not data["year"].isdigit() or not 1900 <= int(data["year"]) <= 2100:
        errors.append("The year must be a number from 1900 to 2100.")
    if data["description"] == "":
        errors.append("The description is required.")
    return data, errors


@app.route("/albums/<int:album_id>")
def album_page(album_id):
    # Сторінка окремого альбому. <int:album_id> - змінна частина адреси.
    album = get_album(album_id)
    # Список пісень зберігається одним текстом, по одній пісні в рядку
    tracks = [track for track in album["tracks"].split("\n") if track.strip() != ""]
    return render_template("album.html", album=album, tracks=tracks)


@app.route("/albums/add", methods=["GET", "POST"])
@login_required
def add_album():
    # Додавання нового альбому (лише для авторизованих користувачів)
    data = {"title": "", "year": "", "description": "", "tracks": ""}
    if request.method == "POST":
        data, errors = read_album_form()
        if errors:
            for error in errors:
                flash(error)
        else:
            db = get_db()
            cursor = db.execute(
                "INSERT INTO albums (title, year, description, tracks) VALUES (?, ?, ?, ?)",
                (data["title"], int(data["year"]), data["description"], data["tracks"]),
            )
            db.commit()
            flash("The album is added.")
            # lastrowid - номер щойно доданого запису
            return redirect(url_for("album_page", album_id=cursor.lastrowid))

    return render_template("album_form.html", album=data, heading="Add album")


@app.route("/albums/<int:album_id>/edit", methods=["GET", "POST"])
@login_required
def edit_album(album_id):
    # Редагування альбому (лише для авторизованих користувачів)
    data = get_album(album_id)
    if request.method == "POST":
        data, errors = read_album_form()
        if errors:
            for error in errors:
                flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE albums SET title = ?, year = ?, description = ?, tracks = ?"
                " WHERE id = ?",
                (data["title"], int(data["year"]), data["description"],
                 data["tracks"], album_id),
            )
            db.commit()
            flash("The album is updated.")
            return redirect(url_for("album_page", album_id=album_id))

    return render_template("album_form.html", album=data, heading="Edit album")


@app.route("/albums/<int:album_id>/delete", methods=["POST"])
@login_required
def delete_album(album_id):
    # Видалення альбому (лише для авторизованих користувачів).
    # Маршрут приймає тільки POST, щоб альбом не можна було видалити
    # простим переходом за посиланням.
    get_album(album_id)
    db = get_db()
    db.execute("DELETE FROM albums WHERE id = ?", (album_id,))
    db.commit()
    flash("The album is deleted.")
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(error):
    # Власна сторінка для помилки 404 (сторінку не знайдено)
    return render_template("404.html"), 404


# Створюємо таблиці під час запуску застосунку (і локально, і на сервері)
with app.app_context():
    init_db()

# Локальний запуск: py app.py, сайт буде доступний за адресою http://127.0.0.1:5000
if __name__ == "__main__":
    app.run(debug=True)
