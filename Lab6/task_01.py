# Лабораторна робота №6. Класи. Частина 1. Завдання 1
# Виконала: Іващук Евеліна

# Завдання 1. Реалізувати клас Person, який відображає запис в книзі
# контактів. Клас має 4 атрибути: surname - прізвище (обов'язковий),
# first_name - ім'я (обов'язковий), nickname - псевдонім (опціональний),
# birth_date - об'єкт datetime.date (обов'язковий). Клас має 2 методи:
# get_age() - рахує вік особи в повних роках на дату виклику і повертає
# рядок виду "25"; get_fullname() - повертає рядок з повним ім'ям
# (прізвище + ім'я) контакту.

import datetime    # модуль для роботи з датами


class Person:
    # Клас описує один запис у книзі контактів

    def __init__(self, surname, first_name, birth_date, nickname=None):
        # Метод __init__ (конструктор) викликається автоматично під час
        # створення екземпляра класу. self - це сам екземпляр, який створюється.
        # Параметр nickname має значення за замовчуванням None, тому він
        # опціональний: його можна не передавати.
        self.surname = surname          # прізвище
        self.first_name = first_name    # ім'я
        self.nickname = nickname        # псевдонім

        # Дата народження передається рядком виду "2002-12-31".
        # Для створення об'єкта datetime.date потрібні три цілі числа:
        # рік, місяць і число. Розбиваємо рядок за символом "-" на три частини
        # і кожну частину перетворюємо в ціле число.
        parts = birth_date.split("-")
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])

        # Створюємо об'єкт datetime.date і зберігаємо його в атрибуті екземпляра
        self.birth_date = datetime.date(year, month, day)

    def get_age(self):
        # Метод повертає вік особи в повних роках на дату виклику у вигляді рядка
        today = datetime.date.today()    # сьогоднішня дата

        # Спочатку рахуємо різницю років
        age = today.year - self.birth_date.year

        # Якщо день народження цього року ще не настав, рік ще не повний
        if today.month < self.birth_date.month:
            age -= 1
        elif today.month == self.birth_date.month and today.day < self.birth_date.day:
            age -= 1

        return str(age)

    def get_fullname(self):
        # Метод повертає повне ім'я контакту: прізвище + ім'я
        return self.surname + " " + self.first_name


# Код нижче виконується тільки тоді, коли цей файл запущено як програму.
# Якщо клас Person імпортують з іншого файла, цей код не виконується.
if __name__ == "__main__":
    # Створюємо два екземпляри класу: з псевдонімом і без нього
    person1 = Person("Kovalenko", "Olena", "2002-12-31", "Lena")
    person2 = Person("Melnyk", "Andrii", "1998-05-17")

    for person in [person1, person2]:
        print("Surname:", person.surname)
        print("First name:", person.first_name)
        print("Nickname:", person.nickname)
        print("Birth date:", person.birth_date, type(person.birth_date))
        print("Full name:", person.get_fullname())
        print("Age:", person.get_age())
        print()
