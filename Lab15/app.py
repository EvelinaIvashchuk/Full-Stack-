# Лабораторна робота №15. Поєднання веб-додатку та машинного навчання
# Виконала: Іващук Евеліна

# Веб-додаток на Flask, який визначає емоцію введеного тексту (sad або happy)
# за допомогою моделі, навченої програмою train_model.py.

import os        # робота зі шляхами до файлів
import pickle    # завантаження збережених об'єктів

from flask import Flask, render_template, request

from preprocess import clean_text    # та сама функція очищення, що й під час навчання

# Файли моделі лежать у тій самій папці, що й програма
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

# Завантажуємо навчену модель і векторизатор один раз під час запуску додатку
with open(os.path.join(BASE_DIR, "model.pkl"), "rb") as file:
    model = pickle.load(file)
with open(os.path.join(BASE_DIR, "vectorizer.pkl"), "rb") as file:
    vectorizer = pickle.load(file)


@app.route("/")
def home():
    # Головна сторінка з формою для введення тексту
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    # Отримуємо текст, який користувач ввів у форму
    text = request.form["message"]
    cleaned = clean_text(text)

    # Якщо після очищення текст порожній, класифікувати нічого
    if cleaned == "":
        return render_template("index.html", message=text,
                               error="Please enter some text in English.")

    # Перетворюємо текст на числовий вектор і передаємо його моделі
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)[0]

    # predict_proba() повертає ймовірності обох класів; беремо більшу з них
    probability = round(model.predict_proba(vector)[0].max() * 100)

    result = "HAPPY" if prediction == 1 else "SAD"

    return render_template("index.html", message=text, result=result,
                           probability=probability)


# Локальний запуск: сайт буде доступний за адресою http://127.0.0.1:5000
if __name__ == "__main__":
    app.run(debug=True)
