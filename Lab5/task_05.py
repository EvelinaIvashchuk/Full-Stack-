# Лабораторна робота №5. Робота з файлами. Завдання 5
# Виконала: Іващук Евеліна

# Завдання 5. Створіть порожній файл guest_book.txt у текстовому редакторі.
# Напишіть програму, яка запитує у користувачів імена. При введенні кожного
# імені виведіть на екран рядок з вітанням для користувача і запишіть рядок
# вітання у файл з ім'ям guest_book.txt. Простежте за тим, щоб кожне
# повідомлення розміщувалося в окремому рядку файла з зазначенням часу
# внесення цього повідомлення. Передбачте зазначення в файлі часу його
# створення і вказання в ньому часу останніх внесених змін.

import os                        # модуль для роботи з файловою системою
from datetime import datetime    # клас для роботи з датою і часом

# Робимо поточним каталог, у якому лежить програма
os.chdir(os.path.dirname(os.path.abspath(__file__)))

FILE_NAME = "guest_book.txt"


def current_time():
    # Функція повертає поточні дату і час у вигляді рядка:
    # рік-місяць-день година:хвилина:секунда
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Читаємо всі рядки, які вже є у файлі (якщо файла немає, список буде порожнім)
lines = []
if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        for line in file:
            lines.append(line.strip())

# Структура файла: 1-й рядок - час створення, 2-й - час останніх змін,
# далі - повідомлення. Якщо файл порожній, часом створення вважаємо поточний час.
if len(lines) == 0:
    created_line = "Guest book created: " + current_time()
    messages = []
else:
    created_line = lines[0]    # час створення залишаємо без змін
    messages = lines[2:]       # повідомлення, записані раніше

# Запитуємо імена, поки користувач не введе порожній рядок
while True:
    name = input("Enter your name (or press Enter to finish): ")
    if name == "":
        break

    greeting = "Hello, " + name + "! Welcome to the guest book!"
    print(greeting)

    # Кожне повідомлення зберігаємо окремим рядком разом з часом його внесення
    messages.append("[" + current_time() + "] " + greeting)

# Записуємо файл заново: час створення, оновлений час останніх змін і всі повідомлення
with open(FILE_NAME, "w", encoding="utf-8") as file:
    file.write(created_line + "\n")
    file.write("Last modified: " + current_time() + "\n")
    for message in messages:
        file.write(message + "\n")

print("The guest book is saved to the file", FILE_NAME)
