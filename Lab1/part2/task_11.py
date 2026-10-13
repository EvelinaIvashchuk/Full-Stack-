# Лабораторна робота №1. Частина 2. Завдання 11
# Виконала: Іващук Евеліна

# Завдання 11. Знайти середнє арифметичне всіх цілих чисел від a до b
# (значення a і b вводяться з клавіатури; a <= b). Вирішити задачу
# використовуючи циклічну конструкцію for.

# Вводимо числа a і b з клавіатури
a = int(input("Enter the number a: "))
b = int(input("Enter the number b (b >= a): "))

# Перевіряємо умову a <= b
if a <= b:
    total = 0    # сума чисел
    count = 0    # кількість чисел

    # range(a, b + 1) дає числа від a до b включно:
    # верхня межа в range не входить, тому пишемо b + 1
    for i in range(a, b + 1):
        total += i    # додаємо чергове число до суми
        count += 1    # збільшуємо кількість чисел на 1

    # Середнє арифметичне - це сума чисел, поділена на їх кількість
    average = total / count

    print("The arithmetic mean of integers from", a, "to", b, "is", average)
else:
    print("Error: a must be less than or equal to b")
