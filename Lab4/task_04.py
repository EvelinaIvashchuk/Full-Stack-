# Лабораторна робота №4. Функції. Завдання 4
# Виконала: Іващук Евеліна

# Завдання 4. Дано числа X, Y, Z, T - довжини сторін чотирикутника.
# Обчислити його площу, якщо кут між сторонами довжиною X і Y - прямий.

import math    # модуль з математичними функціями, потрібна функція sqrt()


def triangle_area(a, b, c):
    # Функція повертає площу трикутника зі сторонами a, b, c за формулою Герона:
    # S = sqrt(p * (p - a) * (p - b) * (p - c)), де p - півпериметр
    p = (a + b + c) / 2
    return math.sqrt(p * (p - a) * (p - b) * (p - c))


# Вводимо довжини сторін чотирикутника
x = float(input("Enter the side X: "))
y = float(input("Enter the side Y: "))
z = float(input("Enter the side Z: "))
t = float(input("Enter the side T: "))

# Діагональ ділить чотирикутник на два трикутники.
# Перший трикутник прямокутний з катетами X і Y, тому діагональ - його гіпотенуза.
d = math.sqrt(x ** 2 + y ** 2)

# Другий трикутник має сторони d, Z, T. Він існує, якщо кожна сторона
# менша за суму двох інших.
if d < z + t and z < d + t and t < d + z:
    # Площа чотирикутника дорівнює сумі площ двох трикутників
    area = triangle_area(x, y, d) + triangle_area(d, z, t)
    print("Diagonal:", round(d, 4))
    print("Area of the quadrilateral:", round(area, 4))
else:
    print("A quadrilateral with such sides does not exist")
