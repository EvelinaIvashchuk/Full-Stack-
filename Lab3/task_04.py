# Лабораторна робота №3. Робота зі списками. Завдання 4
# Виконала: Іващук Евеліна

# Завдання 4. Сформувати список з 30 випадкових цілих чисел від -100 до +100.
# Знайти максимальний елемент списку і його порядковий номер. Отримати інший
# список, що складається тільки з непарних чисел вихідного списку або
# повідомити, що таких чисел немає. Отриманий список вивести в порядку
# зменшення елементів.

import random    # модуль для отримання випадкових чисел

numbers = []    # вихідний список

# Формуємо список з 30 випадкових цілих чисел від -100 до 100
for i in range(30):
    numbers.append(random.randint(-100, 100))

print("List:", numbers)

# Знаходимо максимальний елемент функцією max().
# Метод index() повертає індекс першого входження елемента.
# Порядковий номер на 1 більший за індекс, бо індексація починається з 0.
maximum = max(numbers)
position = numbers.index(maximum) + 1

print("The maximum element:", maximum)
print("Its ordinal number:", position)

odd_numbers = []    # список непарних чисел

# Число непарне, якщо остача від його ділення на 2 не дорівнює 0
for number in numbers:
    if number % 2 != 0:
        odd_numbers.append(number)

# Порожній список має довжину 0 - у такому разі непарних чисел немає
if len(odd_numbers) == 0:
    print("There are no odd numbers in the list")
else:
    # Метод sort() сортує список; reverse=True задає порядок зменшення
    odd_numbers.sort(reverse=True)
    print("Odd numbers in descending order:", odd_numbers)
