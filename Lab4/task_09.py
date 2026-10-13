# Лабораторна робота №4. Функції. Завдання 9
# Виконала: Іващук Евеліна

# Завдання 9. Для завдань 6 - 8 написати декоратор, що дозволить визначати
# час виконання програми. Виконати перевірку часу виконання написаних функцій
# для 10**n елементів при n <= 6 з кроком в n. Тобто визначити час виконання
# функцій для десятків, сотень, тисяч і так до мільйону елементів.

import random    # модуль для отримання випадкових чисел
import time      # модуль для роботи з часом


def timer(function):
    # Декоратор - це функція, яка приймає іншу функцію і повертає нову функцію
    # з додатковою поведінкою. Тут додаємо вимірювання часу виконання.
    def wrapper(*args):
        # *args дозволяє прийняти будь-яку кількість аргументів
        start = time.perf_counter()      # час перед викликом функції
        result = function(*args)         # викликаємо початкову функцію
        end = time.perf_counter()        # час після виконання функції
        # format(..., ".6f") виводить число з шістьма знаками після коми
        print(function.__name__, "- execution time:", format(end - start, ".6f"), "s")
        return result
    return wrapper


# Запис @timer перед функцією означає: find_max_divisors = timer(find_max_divisors)
@timer
def find_max_divisors(m, n):
    # Функція із завдання 6: числа з інтервалу [m, n] з найбільшою кількістю дільників
    counts = [0] * (n - m + 1)
    for d in range(1, n + 1):
        first = ((m + d - 1) // d) * d
        for number in range(first, n + 1, d):
            counts[number - m] += 1

    max_count = max(counts)
    result = []
    for i in range(len(counts)):
        if counts[i] == max_count:
            result.append(m + i)
    return result, max_count


@timer
def find_primes(n):
    # Функція із завдання 7: прості числа від 0 до n (решето Ератосфена).
    # Результат не виводимо, щоб вивід на екран не впливав на виміряний час.
    is_prime = [True] * (n + 1)
    is_prime[0] = False
    if n >= 1:
        is_prime[1] = False

    i = 2
    while i * i <= n:
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
        i += 1

    primes = []
    for i in range(n + 1):
        if is_prime[i]:
            primes.append(i)
    return primes


@timer
def select_values(numbers, bottom, upper):
    # Функція із завдання 8: значення списку від MIN + bottom до MAX - upper
    low = min(numbers) + bottom
    high = max(numbers) - upper
    if bottom < 0 or upper < 0:
        raise ValueError("bottom and upper must not be negative")
    if low > high:
        raise ValueError("the range goes beyond the minimum and maximum values")

    result = []
    for number in numbers:
        if low <= number <= high:
            result.append(number)
    return result


# Перевіряємо час виконання для 10, 100, 1000, ..., 1000000 елементів
for n in range(1, 7):
    size = 10 ** n
    print("Number of elements:", size)

    # Завдання 6: інтервал [1, size] містить size чисел
    find_max_divisors(1, size)

    # Завдання 7: прості числа від 0 до size
    find_primes(size)

    # Завдання 8: список із size випадкових натуральних чисел
    numbers = []
    for i in range(size):
        numbers.append(random.randint(1, 1000))
    select_values(numbers, 10, 10)

    print()    # порожній рядок між результатами
