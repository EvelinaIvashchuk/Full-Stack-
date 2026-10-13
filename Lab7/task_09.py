# Лабораторна робота №7. Класи. Частина 2. Завдання 9
# Виконала: Іващук Евеліна

# Завдання 9. Облік користувачів на сайті. Клас User збережено в модулі
# user.py, класи Privileges і Admin - у модулі admin.py, а ця програма
# імпортує їх і по черзі виконує пункти a-e завдання.

# Пункт e: імпортуємо класи з двох різних модулів
from user import User
from admin import Admin

# a. Створюємо кілька користувачів і для кожного викликаємо обидва методи
print("--- a ---")
user1 = User("Olena", "Kovalenko", "olena@example.com", "lena_k", True)
user2 = User("Andrii", "Melnyk", "andrii@example.com", "andy", False)
user3 = User("Maria", "Shevchenko", "maria@example.com", "masha", True)

for user in [user1, user2, user3]:
    user.describe_user()
    user.greeting_user()

# b. Кілька разів викликаємо increment_login_attempts(), виводимо значення
# login_attempts, потім обнуляємо його методом reset_login_attempts()
print("--- b ---")
user = User("Ivan", "Bondarenko", "ivan@example.com", "ivan_b", False)
user.increment_login_attempts()
user.increment_login_attempts()
user.increment_login_attempts()
print("Login attempts:", user.login_attempts)
user.reset_login_attempts()
print("Login attempts after reset:", user.login_attempts)


# c. Перший варіант класу адміністратора: список привілеїв і метод
# show_privileges() зберігаються в самому класі, що успадковує від User
class SimpleAdmin(User):
    def __init__(self, first_name, last_name, email, nickname, newsletter):
        super().__init__(first_name, last_name, email, nickname, newsletter)
        self.privileges = [
            "Allowed to add message",
            "Allowed to delete users",
            "Allowed to ban users",
        ]

    def show_privileges(self):
        print("Privileges of the administrator:")
        for privilege in self.privileges:
            print("-", privilege)


print("--- c ---")
simple_admin = SimpleAdmin("Sofiia", "Tkachenko", "sofiia@example.com", "sonia", True)
simple_admin.describe_user()
simple_admin.show_privileges()

# d, e. Остаточний варіант: список привілеїв і метод show_privileges()
# перенесено в клас Privileges, екземпляр якого є атрибутом priv класу Admin.
# Класи Admin і Privileges імпортовано з модуля admin.
print("--- d, e ---")
admin = Admin("Sofiia", "Tkachenko", "sofiia@example.com", "sonia", True)
admin.describe_user()
admin.greeting_user()
admin.priv.show_privileges()
