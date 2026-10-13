# Лабораторна робота №1. Частина 2. Завдання 4
# Виконала: Іващук Евеліна

# Завдання 4. Знайти косинус мінімального з 4 заданих чисел.

import math    # підключаємо модуль math, у якому є функція cos()

# Вводимо чотири числа з клавіатури
n1 = float(input("Enter the first number: "))
n2 = float(input("Enter the second number: "))
n3 = float(input("Enter the third number: "))
n4 = float(input("Enter the fourth number: "))

# Шукаємо мінімальне число.
# Спочатку вважаємо мінімальним перше, потім порівнюємо його з рештою:
# якщо наступне число менше, воно стає новим мінімумом.
minimum = n1
if n2 < minimum:
    minimum = n2
if n3 < minimum:
    minimum = n3
if n4 < minimum:
    minimum = n4

# Обчислюємо косинус мінімального числа (аргумент задається в радіанах)
result = math.cos(minimum)

print("The minimum number:", minimum)
print("Cosine of the minimum number:", round(result, 4))
