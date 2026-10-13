# Лабораторна робота №1. Частина 2. Завдання 7
# Виконала: Іващук Евеліна

# Завдання 7. Скласти програму, яка по даному числу (1-12) виводить назву
# відповідного йому місяця англійською мовою.

# Вводимо номер місяця з клавіатури
month = int(input("Enter the month number (1-12): "))

# Перевіряємо номер по черзі: виконується лише та гілка, умова якої істинна
if month == 1:
    print("January")
elif month == 2:
    print("February")
elif month == 3:
    print("March")
elif month == 4:
    print("April")
elif month == 5:
    print("May")
elif month == 6:
    print("June")
elif month == 7:
    print("July")
elif month == 8:
    print("August")
elif month == 9:
    print("September")
elif month == 10:
    print("October")
elif month == 11:
    print("November")
elif month == 12:
    print("December")
else:
    # Якщо число не входить у діапазон 1-12, повідомляємо про помилку
    print("Error: the month number must be from 1 to 12")
