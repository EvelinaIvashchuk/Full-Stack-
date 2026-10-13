# Лабораторна робота №1. Частина 2. Завдання 9
# Виконала: Іващук Евеліна

# Завдання 9. Дано два числа A і B (A < B). Знайти суму всіх цілих чисел
# від A до B включно. Вирішити задачу використовуючи циклічну конструкцію for.

# Вводимо числа A і B з клавіатури
a = int(input("Enter the number A: "))
b = int(input("Enter the number B (B > A): "))

# Перевіряємо умову A < B
if a < b:
    total = 0    # змінна для накопичення суми, спочатку дорівнює 0

    # range(a, b + 1) дає числа від a до b включно:
    # верхня межа в range не входить, тому пишемо b + 1
    for i in range(a, b + 1):
        total += i    # додаємо чергове число до суми

    print("The sum of integers from", a, "to", b, "is", total)
else:
    print("Error: A must be less than B")
