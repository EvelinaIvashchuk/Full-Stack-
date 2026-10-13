# Лабораторна робота №9. Unit-тестування в мові Python
# Виконала: Іващук Евеліна

# Тести для класу User (модуль user.py) та класів Privileges і Admin
# (модуль admin.py), написані за допомогою фреймворку unittest.

import contextlib    # засоби для тимчасового перенаправлення виводу
import io            # клас StringIO - "файл" у пам'яті, в який можна писати текст
import unittest      # фреймворк для unit-тестування

from user import User                  # класи, які тестуємо
from admin import Admin, Privileges


def get_output(function):
    # Допоміжна функція: викликає передану функцію і повертає текст,
    # який вона вивела на екран функцією print()
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        function()
    return buffer.getvalue()


class TestUser(unittest.TestCase):

    def setUp(self):
        # Перед кожним тестом створюємо нового користувача
        self.user = User("Olena", "Kovalenko", "olena@example.com", "lena_k", True)

    def test_attributes(self):
        # Конструктор має зберегти всі дані профілю в атрибутах
        self.assertEqual(self.user.first_name, "Olena")
        self.assertEqual(self.user.last_name, "Kovalenko")
        self.assertEqual(self.user.email, "olena@example.com")
        self.assertEqual(self.user.nickname, "lena_k")
        self.assertTrue(self.user.newsletter)

    def test_describe_user(self):
        # Метод describe_user() має вивести повне ім'я користувача
        output = get_output(self.user.describe_user)
        self.assertIn("Olena Kovalenko", output)

    def test_greeting_user(self):
        # Метод greeting_user() має привітати користувача за нікнеймом
        output = get_output(self.user.greeting_user)
        self.assertIn("Hello, lena_k!", output)

    def test_greeting_user_without_nickname(self):
        # Якщо нікнейм порожній, у вітанні має бути ім'я користувача
        user = User("Andrii", "Melnyk", "andrii@example.com", "", False)
        output = get_output(user.greeting_user)
        self.assertIn("Hello, Andrii!", output)

    def test_default_login_attempts(self):
        # Кількість спроб входу спочатку дорівнює 0
        self.assertEqual(self.user.login_attempts, 0)

    def test_increment_login_attempts(self):
        # Кожен виклик методу збільшує кількість спроб входу на 1
        self.user.increment_login_attempts()
        self.assertEqual(self.user.login_attempts, 1)
        self.user.increment_login_attempts()
        self.user.increment_login_attempts()
        self.assertEqual(self.user.login_attempts, 3)

    def test_reset_login_attempts(self):
        # Метод reset_login_attempts() обнуляє кількість спроб входу
        self.user.increment_login_attempts()
        self.user.increment_login_attempts()
        self.user.reset_login_attempts()
        self.assertEqual(self.user.login_attempts, 0)

    def test_users_are_independent(self):
        # Спроби входу одного користувача не впливають на іншого
        other = User("Maria", "Shevchenko", "maria@example.com", "masha", True)
        self.user.increment_login_attempts()
        self.assertEqual(other.login_attempts, 0)


class TestPrivileges(unittest.TestCase):

    def test_privileges_list(self):
        # Атрибут privileges має містити список привілеїв адміністратора
        priv = Privileges()
        self.assertIn("Allowed to add message", priv.privileges)
        self.assertIn("Allowed to delete users", priv.privileges)
        self.assertIn("Allowed to ban users", priv.privileges)

    def test_show_privileges(self):
        # Метод show_privileges() має вивести кожен привілей
        priv = Privileges()
        output = get_output(priv.show_privileges)
        for privilege in priv.privileges:
            self.assertIn(privilege, output)


class TestAdmin(unittest.TestCase):

    def setUp(self):
        self.admin = Admin("Sofiia", "Tkachenko", "sofiia@example.com", "sonia", True)

    def test_is_user(self):
        # Клас Admin успадковує від User
        self.assertIsInstance(self.admin, User)

    def test_inherited_attributes(self):
        # Атрибути класу User мають бути створені і в адміністратора
        self.assertEqual(self.admin.first_name, "Sofiia")
        self.assertEqual(self.admin.last_name, "Tkachenko")
        self.assertEqual(self.admin.login_attempts, 0)

    def test_inherited_methods(self):
        # Методи класу User мають працювати і для адміністратора
        output = get_output(self.admin.describe_user)
        self.assertIn("Sofiia Tkachenko", output)
        self.admin.increment_login_attempts()
        self.assertEqual(self.admin.login_attempts, 1)

    def test_priv_attribute(self):
        # Атрибут priv має бути екземпляром класу Privileges
        self.assertIsInstance(self.admin.priv, Privileges)

    def test_show_privileges(self):
        # Привілеї адміністратора виводяться через атрибут priv
        output = get_output(self.admin.priv.show_privileges)
        self.assertIn("Allowed to ban users", output)

    def test_admins_have_own_privileges(self):
        # Кожен адміністратор має власний список привілеїв:
        # зміна списку одного адміністратора не впливає на іншого
        other = Admin("Ivan", "Bondarenko", "ivan@example.com", "ivan_b", False)
        self.admin.priv.privileges.append("Allowed to edit settings")
        self.assertNotIn("Allowed to edit settings", other.priv.privileges)


# Якщо файл запущено як програму, запускаємо всі тести з докладним виводом
if __name__ == "__main__":
    unittest.main(verbosity=2)
