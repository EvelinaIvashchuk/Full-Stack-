# Лабораторна робота №4. Функції. Завдання 5
# Виконала: Іващук Евеліна

# Завдання 5. Знайти всі натуральні числа, що не перевищують заданого n,
# які діляться на кожне із заданих користувачем чисел.


def is_divisible_by_all(number, divisors):
    # Функція повертає True, якщо number ділиться без остачі на кожне число
    # зі списку divisors, інакше повертає False
    for divisor in divisors:
        if number % divisor != 0:
            return False    # знайшли число, на яке не ділиться - далі не перевіряємо
    return True


# Вводимо число n
n = int(input("Enter the number n: "))

# Вводимо дільники одним рядком через пробіл.
# split() розбиває рядок на частини, кожну частину перетворюємо в ціле число.
divisors = []
for part in input("Enter the divisors separated by spaces: ").split():
    divisors.append(int(part))

result = []    # список знайдених чисел

# На нуль ділити не можна, тому нуль серед дільників вважаємо помилкою введення
if len(divisors) == 0 or 0 in divisors:
    print("Error: enter at least one divisor, zero is not allowed")
else:
    # Перебираємо всі натуральні числа від 1 до n включно
    for number in range(1, n + 1):
        if is_divisible_by_all(number, divisors):
            result.append(number)

    if len(result) == 0:
        print("There are no such numbers")
    else:
        print("Numbers divisible by", divisors, ":", result)
