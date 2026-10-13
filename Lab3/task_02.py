# Лабораторна робота №3. Робота зі списками. Завдання 2
# Виконала: Іващук Евеліна

# Завдання 2. Дано список, що складається з N цілочисельних елементів. Список
# вводиться з клавіатури. Переписати всі додатні елементи в другий масив,
# а решту - в третій.

# Вводимо кількість елементів списку
n = int(input("Enter the number of elements N: "))

numbers = []    # початковий список

# Вводимо N чисел і кожне додаємо в кінець списку
for i in range(n):
    number = int(input("Enter element " + str(i + 1) + ": "))
    numbers.append(number)

positive = []    # другий список - для додатних елементів
others = []      # третій список - для решти елементів (від'ємних і нулів)

# Перебираємо елементи початкового списку і розподіляємо їх по двох списках
for number in numbers:
    if number > 0:
        positive.append(number)
    else:
        others.append(number)

print("Initial list:", numbers)
print("Positive elements:", positive)
print("Other elements:", others)
