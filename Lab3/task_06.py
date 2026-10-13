# Лабораторна робота №3. Робота зі списками. Завдання 6
# Виконала: Іващук Евеліна

# Завдання 6. Дано список з 10 цілих чисел. Знайти максимальний елемент і
# порівняти з ним інші елементи. Квадрати менших чисел записати в другий
# список в порядку зменшення.

import random    # модуль для отримання випадкових чисел

numbers = []    # початковий список

# Заповнюємо список 10 випадковими цілими числами від -100 до 100
for i in range(10):
    numbers.append(random.randint(-100, 100))

print("List:", numbers)

# Знаходимо максимальний елемент
maximum = max(numbers)
print("The maximum element:", maximum)

squares = []    # другий список - для квадратів менших чисел

# Порівнюємо кожен елемент з максимальним:
# якщо елемент менший, записуємо його квадрат у другий список
for number in numbers:
    if number < maximum:
        squares.append(number ** 2)

# Сортуємо другий список у порядку зменшення
squares.sort(reverse=True)

print("Squares of smaller numbers in descending order:", squares)
