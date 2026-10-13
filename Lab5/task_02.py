# Лабораторна робота №5. Робота з файлами. Завдання 2
# Виконала: Іващук Евеліна

# Завдання 2. Реалізуйте програму, яка зчитує довільну кількість цілих чисел,
# що вводяться з командного рядка, і записує у текстовий файл інформацію
# щодо парності або непарності чисел.

import os     # модуль для роботи з файловою системою
import sys    # модуль, що дає доступ до аргументів командного рядка

# Робимо поточним каталог, у якому лежить програма
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# sys.argv - список аргументів командного рядка. Перший елемент - назва
# програми, тому самі числа починаються з індексу 1.
# Приклад запуску: py task_02.py 4 7 10 -3
values = sys.argv[1:]

# Якщо програму запущено без аргументів (наприклад, з IDLE),
# просимо ввести числа одним рядком через пробіл
if len(values) == 0:
    values = input("Enter integers separated by spaces: ").split()

# Відкриваємо файл для запису
with open("even_odd.txt", "w", encoding="utf-8") as file:
    for value in values:
        # int() створює виняток ValueError, якщо введено не ціле число
        try:
            number = int(value)
            if number % 2 == 0:
                line = str(number) + " - even"
            else:
                line = str(number) + " - odd"
        except ValueError:
            line = value + " - not an integer"

        print(line)                # виводимо рядок на екран
        file.write(line + "\n")    # і записуємо його у файл

print("The result is saved to the file even_odd.txt")
