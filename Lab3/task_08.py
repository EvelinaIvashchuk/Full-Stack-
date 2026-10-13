# Лабораторна робота №3. Робота зі списками. Завдання 8
# Виконала: Іващук Евеліна

# Завдання 8. Дано список з 30 випадкових цілих і дробових чисел від -100 до
# +100. Сформувати зі списку 10 списків по 3 елементи. Вивести отримані
# списки в порядку зростання за сумою абсолютних значень окремих елементів.

import random    # модуль для отримання випадкових чисел


def abs_sum(items):
    # Функція повертає суму абсолютних значень (модулів) елементів списку
    total = 0
    for item in items:
        total += abs(item)
    return total


numbers = []    # початковий список

# Формуємо список з 30 чисел: тип кожного числа обираємо випадково
for i in range(30):
    if random.choice(["int", "float"]) == "int":
        numbers.append(random.randint(-100, 100))
    else:
        numbers.append(round(random.uniform(-100, 100), 2))

print("List:", numbers)

groups = []    # список, елементами якого є 10 списків по 3 елементи

# range(0, 30, 3) дає індекси 0, 3, 6, ..., 27 - початок кожної трійки.
# Зріз numbers[i:i + 3] повертає список з трьох елементів, починаючи з індексу i.
for i in range(0, 30, 3):
    groups.append(numbers[i:i + 3])

# Сортуємо списки за сумою модулів їх елементів.
# Параметр key задає функцію, за значенням якої порівнюються елементи.
groups.sort(key=abs_sum)

print("Lists in ascending order of the sum of absolute values:")
for group in groups:
    print(group, "- sum:", round(abs_sum(group), 2))
