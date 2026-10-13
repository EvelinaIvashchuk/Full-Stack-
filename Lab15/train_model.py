# Лабораторна робота №15. Поєднання веб-додатку та машинного навчання
# Виконала: Іващук Евеліна

# Варіант 5. Text Emotion Recognition: навчання моделі, яка визначає емоцію
# тексту - sad (сумний) або happy (радісний). Програма запускається один раз;
# її результат - файли model.pkl і vectorizer.pkl, які використовує веб-додаток.

import os        # робота зі шляхами до файлів
import pickle    # збереження об'єктів Python у файл

import pandas as pd    # робота з табличними даними
from sklearn.feature_extraction.text import TfidfVectorizer    # текст -> числа
from sklearn.linear_model import LogisticRegression            # модель класифікації
from sklearn.metrics import classification_report              # звіт про якість
from sklearn.model_selection import train_test_split           # розбиття даних

from preprocess import clean_text    # функція очищення тексту

# Робимо поточним каталог, у якому лежить програма, щоб файли шукалися поруч з нею
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 1. Завантаження датасету.
# Файл train.csv містить два стовпці: text - текст, emotion - мітка класу
# (0 - sad, 1 - happy). Для зручності перейменовуємо стовпці.
df = pd.read_csv("train.csv")
df.columns = ["message", "label"]

print("Number of texts:", len(df))
print("Texts labelled sad (0):", (df["label"] == 0).sum())
print("Texts labelled happy (1):", (df["label"] == 1).sum())

# Очищаємо кожен текст: метод apply() викликає функцію для кожного рядка стовпця
df["message"] = df["message"].astype(str).apply(clean_text)

# 2. Розбиття на навчальну (80%) і тестову (20%) вибірки.
# random_state=42 робить розбиття однаковим під час кожного запуску.
X_train, X_test, y_train, y_test = train_test_split(
    df["message"], df["label"], test_size=0.2, random_state=42
)

# 3. Векторизація тексту методом TF-IDF: кожен текст перетворюється на числовий
# вектор. ngram_range=(1, 2) означає, що враховуються окремі слова і пари слів,
# min_df=5 відкидає слова, які зустрічаються менш ніж у п'яти текстах.
# Стоп-слова не вилучаються, бо серед них є заперечення "not", важливе для емоцій.
vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=5)
X_train_vec = vectorizer.fit_transform(X_train)    # навчаємо векторизатор і перетворюємо
X_test_vec = vectorizer.transform(X_test)          # тестові дані лише перетворюємо

print("Number of features:", X_train_vec.shape[1])

# 4. Навчання моделі логістичної регресії.
# max_iter=1000 - найбільша кількість кроків навчання.
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

# Перевіряємо якість моделі на тестових даних, яких вона не бачила під час навчання
print("Accuracy:", round(model.score(X_test_vec, y_test), 4))
print(classification_report(y_test, model.predict(X_test_vec),
                            target_names=["sad", "happy"]))

# 5. Збереження моделі та векторизатора у файли
with open("model.pkl", "wb") as file:
    pickle.dump(model, file)
with open("vectorizer.pkl", "wb") as file:
    pickle.dump(vectorizer, file)

print("The model and the vectorizer are saved!")
