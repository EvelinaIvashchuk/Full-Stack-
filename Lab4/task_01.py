# Лабораторна робота №4. Функції. Завдання 1
# Виконала: Іващук Евеліна

# Завдання 1. Користувач вводить дві сторони трьох прямокутників.
# Вивести їх площі.


def rectangle_area(a, b):
    # Функція приймає дві сторони прямокутника і повертає його площу
    return a * b


# Повторюємо введення і обчислення для кожного з трьох прямокутників
for i in range(1, 4):
    print("Rectangle", i)
    side_a = float(input("Enter the first side: "))
    side_b = float(input("Enter the second side: "))

    # Викликаємо функцію і виводимо значення, яке вона повернула
    print("Area of rectangle", i, ":", rectangle_area(side_a, side_b))
