# Лабораторна робота №4. Функції. Завдання 2
# Виконала: Іващук Евеліна

# Завдання 2. Дано катети двох прямокутних трикутників. Написати функцію
# обчислення довжини гіпотенузи цих трикутників. Порівняти і вивести, яка з
# гіпотенуз більше, а яка менше.

import math    # модуль з математичними функціями, потрібна функція sqrt()


def hypotenuse(a, b):
    # Функція повертає довжину гіпотенузи за теоремою Піфагора: c = sqrt(a^2 + b^2)
    return math.sqrt(a ** 2 + b ** 2)


# Вводимо катети першого трикутника
a1 = float(input("Enter the first leg of triangle 1: "))
b1 = float(input("Enter the second leg of triangle 1: "))

# Вводимо катети другого трикутника
a2 = float(input("Enter the first leg of triangle 2: "))
b2 = float(input("Enter the second leg of triangle 2: "))

# Одну й ту саму функцію викликаємо двічі з різними аргументами
c1 = hypotenuse(a1, b1)
c2 = hypotenuse(a2, b2)

print("Hypotenuse of triangle 1:", round(c1, 4))
print("Hypotenuse of triangle 2:", round(c2, 4))

# Порівнюємо гіпотенузи
if c1 > c2:
    print("The hypotenuse of triangle 1 is greater, of triangle 2 is smaller")
elif c1 < c2:
    print("The hypotenuse of triangle 2 is greater, of triangle 1 is smaller")
else:
    print("The hypotenuses are equal")
