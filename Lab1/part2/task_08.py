# Лабораторна робота №1. Частина 2. Завдання 8
# Виконала: Іващук Евеліна

# Завдання 8. Дано три числа. Знайти кількість позитивних чисел серед них.

# Вводимо три числа з клавіатури
n1 = float(input("Enter the first number: "))
n2 = float(input("Enter the second number: "))
n3 = float(input("Enter the third number: "))

# Лічильник позитивних (додатних) чисел, спочатку дорівнює 0
count = 0

# Кожне число перевіряємо окремо: якщо воно більше 0, збільшуємо лічильник на 1
if n1 > 0:
    count += 1
if n2 > 0:
    count += 1
if n3 > 0:
    count += 1

print("Number of positive numbers:", count)
