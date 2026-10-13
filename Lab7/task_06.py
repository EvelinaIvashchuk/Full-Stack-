# Лабораторна робота №7. Класи. Частина 2. Завдання 6
# Виконала: Іващук Евеліна

# Завдання 6. Напишіть клас-виняток на основі вбудованого в Python класу
# ValueError(). Клас буде представляти перевірку певного імені на основі
# його довжини. Якщо довжина введеного імені є меншою 10, то має генеруватися
# виняток. У інших випадках нічого не виводиться.


# Власний клас-виняток успадковує від вбудованого класу ValueError
class NameTooShortError(ValueError):
    def __init__(self, name):
        # Зберігаємо ім'я в атрибуті винятку
        self.name = name

        # Викликаємо конструктор батьківського класу і передаємо йому
        # текст повідомлення, яке буде показано разом з винятком
        message = "the name '" + name + "' is too short: " + str(len(name))
        message += " characters, at least 10 are required"
        super().__init__(message)


def check_name(name):
    # Функція перевіряє довжину імені: якщо вона менша за 10,
    # оператор raise генерує виняток
    if len(name) < 10:
        raise NameTooShortError(name)


name = input("Enter the name: ")
check_name(name)
