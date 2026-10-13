# Лабораторна робота №5. Робота з файлами. Завдання 6
# Виконала: Іващук Евеліна

# Завдання 6. Збережіть в текстовому файлі публікацію про Python на 3000 слів
# англійською мовою. Напишіть програму, що аналізуватиме частоту, з якою в
# тексті зустрічатимуться окремі літери чи слова незалежно від їх регістру.
# Результат роботи програми має виводитись в консоль і зберігатись в
# окремому файлі з зазначенням часу його створення, часу виконання окремих
# змін, результатів пошуку і часу, що знадобився на виконання цього пошуку.

import os                        # модуль для роботи з файловою системою
import time                      # модуль для вимірювання часу виконання
from datetime import datetime    # клас для роботи з датою і часом

# Робимо поточним каталог, у якому лежить програма
os.chdir(os.path.dirname(os.path.abspath(__file__)))

TEXT_FILE = "python_article.txt"
RESULT_FILE = "search_results.txt"


def current_time():
    # Функція повертає поточні дату і час у вигляді рядка
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Читаємо весь текст публікації і переводимо його в нижній регістр,
# щоб пошук не залежав від регістру літер
with open(TEXT_FILE, "r", encoding="utf-8") as file:
    text = file.read().lower()

# Готуємо дані для пошуку: залишаємо в тексті тільки літери, решту символів
# замінюємо пробілами, після чого розбиваємо текст на слова
cleaned = ""
for char in text:
    if char.isalpha():
        cleaned += char
    else:
        cleaned += " "
words = cleaned.split()

# Загальна кількість літер у тексті (пробіли не рахуємо)
letters_total = len(cleaned.replace(" ", ""))

print("Words in the text:", len(words))
print("Letters in the text:", letters_total)

# Якщо файла результатів ще немає, створюємо його і записуємо час створення
if not os.path.exists(RESULT_FILE):
    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        file.write("File created: " + current_time() + "\n")

# Виконуємо пошук, поки користувач не введе порожній рядок
while True:
    query = input("Enter a letter or a word (or press Enter to finish): ").lower()
    if query == "":
        break

    start = time.perf_counter()    # час початку пошуку

    if len(query) == 1:
        # Одна літера: рахуємо, скільки разів вона зустрічається в тексті
        kind = "letter"
        count = cleaned.count(query)
        percent = count / letters_total * 100
    else:
        # Слово: рахуємо, скільки елементів списку слів дорівнюють шуканому
        kind = "word"
        count = words.count(query)
        percent = count / len(words) * 100

    search_time = time.perf_counter() - start    # тривалість пошуку в секундах

    result = kind + " '" + query + "': found " + str(count) + " times, frequency "
    result += str(round(percent, 2)) + "%, search time "
    result += format(search_time, ".6f") + " s"    # час із шістьма знаками після коми
    print(result)

    # Режим "a" (append) додає рядок у кінець файла, не стираючи попередні записи.
    # Перед результатом записуємо час, коли було внесено цю зміну.
    with open(RESULT_FILE, "a", encoding="utf-8") as file:
        file.write("[" + current_time() + "] " + result + "\n")

print("The results are saved to the file", RESULT_FILE)
