# Лабораторна робота №3. Робота зі списками. Завдання 7
# Виконала: Іващук Евеліна

# Завдання 7. Дано список з 30 випадкових цілих і дробових чисел від -100 до
# +100. Знайти та вивести мінімальний по модулю елемент. Вивести список на
# екран в порядку збільшення значення.

import random    # модуль для отримання випадкових чисел

numbers = []    # порожній список

# Формуємо список з 30 чисел: тип кожного числа обираємо випадково.
# random.choice() повертає випадковий елемент з переданого списку.
for i in range(30):
    if random.choice(["int", "float"]) == "int":
        # ціле число від -100 до 100
        numbers.append(random.randint(-100, 100))
    else:
        # uniform(a, b) повертає випадкове дробове число від a до b;
        # round(..., 2) округлює його до двох знаків після коми
        numbers.append(round(random.uniform(-100, 100), 2))

print("List:", numbers)

# Шукаємо мінімальний по модулю елемент.
# Спочатку вважаємо таким перший елемент, потім порівнюємо модулі решти:
# abs() повертає модуль (абсолютне значення) числа.
min_abs = numbers[0]
for number in numbers:
    if abs(number) < abs(min_abs):
        min_abs = number

print("The element with the minimum absolute value:", min_abs)

# Функція sorted() повертає новий список, відсортований у порядку збільшення
sorted_numbers = sorted(numbers)
print("List in ascending order:", sorted_numbers)
