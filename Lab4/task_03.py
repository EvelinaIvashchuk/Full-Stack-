# Лабораторна робота №4. Функції. Завдання 3
# Виконала: Іващук Евеліна

# Завдання 3. Задано коло (x-a)^2 + (y-b)^2 = R^2 і точки P(p1, p2),
# F(f1, f2), L(l1, l2). З'ясувати і вивести на екран, скільки точок лежить
# всередині кола. Перевірку, чи лежить точка всередині кола, оформити у
# вигляді функції.


def is_inside(x, y, a, b, r):
    # Функція повертає True, якщо точка (x, y) лежить всередині кола
    # з центром (a, b) і радіусом r, інакше повертає False.
    # Точка всередині кола, якщо квадрат відстані до центру менший за R^2.
    return (x - a) ** 2 + (y - b) ** 2 < r ** 2


# Вводимо параметри кола: координати центру і радіус
a = float(input("Enter the x coordinate of the center (a): "))
b = float(input("Enter the y coordinate of the center (b): "))
r = float(input("Enter the radius R: "))

# Вводимо координати трьох точок
p1 = float(input("Enter p1: "))
p2 = float(input("Enter p2: "))
f1 = float(input("Enter f1: "))
f2 = float(input("Enter f2: "))
l1 = float(input("Enter l1: "))
l2 = float(input("Enter l2: "))

count = 0    # кількість точок усередині кола

# Для кожної точки викликаємо функцію; якщо вона повернула True, збільшуємо лічильник
if is_inside(p1, p2, a, b, r):
    count += 1
if is_inside(f1, f2, a, b, r):
    count += 1
if is_inside(l1, l2, a, b, r):
    count += 1

print("Number of points inside the circle:", count)
