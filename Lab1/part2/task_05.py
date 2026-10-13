# Лабораторна робота №1. Частина 2. Завдання 5
# Виконала: Іващук Евеліна

# Завдання 5. Вивести на екран синус максимального з 3 заданих чисел.

import math    # підключаємо модуль math, у якому є функція sin()

# Вводимо три числа з клавіатури
n1 = float(input("Enter the first number: "))
n2 = float(input("Enter the second number: "))
n3 = float(input("Enter the third number: "))

# Шукаємо максимальне число.
# Спочатку вважаємо максимальним перше, потім порівнюємо його з рештою:
# якщо наступне число більше, воно стає новим максимумом.
maximum = n1
if n2 > maximum:
    maximum = n2
if n3 > maximum:
    maximum = n3

# Обчислюємо синус максимального числа (аргумент задається в радіанах)
result = math.sin(maximum)

print("The maximum number:", maximum)
print("Sine of the maximum number:", round(result, 4))
