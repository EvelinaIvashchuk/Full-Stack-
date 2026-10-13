# Лабораторна робота №9. Unit-тестування в мові Python
# Виконала: Іващук Евеліна

# Модуль admin містить класи Privileges і Admin для завдання 9

# Клас User імпортуємо з модуля user (файл user.py у цій самій папці)
from user import User


class Privileges:
    # Клас зберігає список привілеїв адміністратора

    def __init__(self):
        self.privileges = [
            "Allowed to add message",
            "Allowed to delete users",
            "Allowed to ban users",
        ]

    def show_privileges(self):
        # Метод виводить набір привілеїв адміністратора
        print("Privileges of the administrator:")
        for privilege in self.privileges:
            print("-", privilege)


class Admin(User):
    # Адміністратор - користувач з повними адміністративними привілеями.
    # Клас успадковує від класу User.

    def __init__(self, first_name, last_name, email, nickname, newsletter):
        # Викликаємо конструктор батьківського класу User
        super().__init__(first_name, last_name, email, nickname, newsletter)

        # Екземпляр класу Privileges зберігаємо як атрибут priv:
        # об'єкт одного класу є частиною об'єкта іншого класу
        self.priv = Privileges()
