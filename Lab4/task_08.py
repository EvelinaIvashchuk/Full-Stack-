# Лабораторна робота №4. Функції. Завдання 8
# Виконала: Іващук Евеліна

# Завдання 8. Дано список з випадкових натуральних чисел довільної довжини.
# Написати програму, що формуватиме з заданого другий список, що міститиме
# тільки значення від MIN+bottom до MAX-upper. Де MIN і MAX - відповідно
# найменше і найбільше число в списку, а bottom і upper - нижня і верхня межа
# значень вибірки нового списку. Програма має містити обробку винятків на
# випадок введення символів невірного типу, дробових чисел, вихід за межі
# мінімального і максимального значення.

import random    # модуль для отримання випадкових чисел


def select_values(numbers, bottom, upper):
    # Функція повертає новий список, що містить тільки значення
    # від MIN + bottom до MAX - upper включно
    low = min(numbers) + bottom     # нижня межа вибірки
    high = max(numbers) - upper     # верхня межа вибірки

    # Оператор raise створює виняток, якщо межі задано неправильно
    if bottom < 0 or upper < 0:
        raise ValueError("bottom and upper must not be negative")
    if low > high:
        raise ValueError("the range goes beyond the minimum and maximum values")

    result = []
    for number in numbers:
        if low <= number <= high:
            result.append(number)
    return result


# У блоці try виконуємо код, у якому може виникнути виняток
try:
    # int() створює виняток ValueError, якщо введено літери або дробове число
    length = int(input("Enter the length of the list: "))
    if length <= 0:
        raise ValueError("the length must be a natural number")

    # Формуємо список випадкових натуральних чисел від 1 до 100
    numbers = []
    for i in range(length):
        numbers.append(random.randint(1, 100))

    print("List:", numbers)
    print("MIN =", min(numbers), ", MAX =", max(numbers))

    bottom = int(input("Enter bottom: "))
    upper = int(input("Enter upper: "))

    result = select_values(numbers, bottom, upper)
    print("Values from", min(numbers) + bottom, "to", max(numbers) - upper, ":", result)

# Блок except виконується, якщо в блоці try виник виняток ValueError
except ValueError as error:
    print("Error:", error)
