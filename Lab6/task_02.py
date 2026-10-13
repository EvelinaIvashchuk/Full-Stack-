# Лабораторна робота №6. Класи. Частина 1. Завдання 2
# Виконала: Іващук Евеліна

# Завдання 2. Написати функцію modifier(filename), яка приймає ім'я файлу і
# повинна: прочитати дані з переданого файлу; створити об'єкти класу Person
# на підставі отриманих даних; модифікувати дані в файлі: а) додати графу
# повного імені (fullname) після графи з ім'ям (name); б) додати графу з
# віком (age) в кінець. На виході отримати файл, розширений зазначеним чином.

import csv    # модуль для роботи з файлами у форматі CSV
import os     # модуль для роботи з файловою системою

# Імпортуємо клас Person з файла task_01.py, який лежить у цій самій папці
from task_01 import Person

# Робимо поточним каталог, у якому лежить програма
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def modifier(filename):
    # Функція читає контакти з файла, створює об'єкти класу Person
    # і записує файл заново з графами fullname та age

    # Читаємо дані. csv.DictReader перетворює кожен рядок файла на словник,
    # у якому ключами є назви граф з першого рядка (заголовка).
    # newline="" потрібен модулю csv для правильної обробки кінців рядків.
    persons = []    # список об'єктів класу Person
    with open(filename, "r", encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            # Створюємо об'єкт класу Person з даних одного рядка файла
            person = Person(row["surname"], row["name"],
                            row["birth_date"], row["nickname"])
            persons.append(person)

    # Записуємо файл заново: графа fullname стоїть після name, графа age - в кінці
    with open(filename, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        # writerow() записує один рядок таблиці зі списку значень
        writer.writerow(["surname", "name", "fullname", "nickname", "birth_date", "age"])
        for person in persons:
            writer.writerow([
                person.surname,
                person.first_name,
                person.get_fullname(),    # повне ім'я повертає метод класу
                person.nickname,
                person.birth_date,
                person.get_age(),         # вік повертає метод класу
            ])

    return len(persons)


def print_file(filename):
    # Допоміжна функція: виводить вміст файла на екран
    with open(filename, "r", encoding="utf-8") as file:
        print(file.read().strip())


print("File before modification:")
print_file("contacts.csv")

count = modifier("contacts.csv")

print()
print("File after modification:")
print_file("contacts.csv")

print()
print("Number of contacts:", count)
