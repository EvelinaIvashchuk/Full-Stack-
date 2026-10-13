# Лабораторна робота №9. Unit-тестування в мові Python
# Виконала: Іващук Евеліна

# Модуль user містить клас User для завдання 9 "Облік користувачів на сайті"


class User:
    # Клас описує користувача сайту

    def __init__(self, first_name, last_name, email, nickname, newsletter):
        self.first_name = first_name    # ім'я
        self.last_name = last_name      # прізвище
        self.email = email              # поштова адреса
        self.nickname = nickname        # нікнейм, що відображається на сайті
        self.newsletter = newsletter    # згода на розсилку новин (True або False)
        self.login_attempts = 0         # кількість спроб входу

    def describe_user(self):
        # Метод виводить повне ім'я користувача
        print("User:", self.first_name, self.last_name)

    def greeting_user(self):
        # Метод виводить персональне вітання для користувача.
        # Виправлено за результатами тестування: якщо нікнейм порожній,
        # у вітанні використовуємо ім'я користувача.
        name = self.nickname
        if name == "":
            name = self.first_name
        print("Hello,", name + "! Welcome back to the site!")

    def increment_login_attempts(self):
        # Метод збільшує кількість спроб входу на 1
        self.login_attempts += 1

    def reset_login_attempts(self):
        # Метод обнуляє кількість спроб входу
        self.login_attempts = 0
