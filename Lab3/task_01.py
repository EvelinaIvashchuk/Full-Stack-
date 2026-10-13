# Лабораторна робота №3. Робота зі списками. Завдання 1
# Виконала: Іващук Евеліна

# Завдання 1. Дано список, що складається з N цілочисельних елементів. Список
# вводиться з клавіатури. Знайти максимальний елемент. Вивести список на
# екран у зворотному порядку.

# Вводимо кількість елементів списку
n = int(input("Enter the number of elements N: "))

numbers = []    # порожній список для чисел

# Вводимо N чисел і кожне додаємо в кінець списку методом append()
for i in range(n):
    number = int(input("Enter element " + str(i + 1) + ": "))
    numbers.append(number)

print("List:", numbers)

# У порожньому списку немає максимального елемента, тому перевіряємо його довжину
if len(numbers) == 0:
    print("The list is empty")
else:
    # Вбудована функція max() повертає найбільший елемент списку
    maximum = max(numbers)
    print("The maximum element:", maximum)

    # Зріз [::-1] повертає новий список з елементами у зворотному порядку
    reversed_numbers = numbers[::-1]
    print("List in reverse order:", reversed_numbers)
