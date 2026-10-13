# Лабораторна робота №1. Частина 2. Завдання 1
# Виконала: Іващук Евеліна

# Завдання 1. Дано три цілих числа. Вибрати з них ті, які належать інтервалу [1,3].

# Вводимо три цілих числа з клавіатури
x = int(input("Enter the first integer number: "))
y = int(input("Enter the second integer number: "))
z = int(input("Enter the third integer number: "))

print("Numbers that belong to the interval [1, 3]:")

# Кожне число перевіряємо окремим оператором if.
# Умова 1 <= x <= 3 означає: x не менше 1 і не більше 3.
if 1 <= x <= 3:
    print(x)
if 1 <= y <= 3:
    print(y)
if 1 <= z <= 3:
    print(z)

# Якщо жодне число не належить інтервалу, повідомляємо про це
if not (1 <= x <= 3) and not (1 <= y <= 3) and not (1 <= z <= 3):
    print("None of the numbers belong to the interval [1, 3]")
