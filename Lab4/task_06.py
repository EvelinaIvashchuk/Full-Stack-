# Лабораторна робота №4. Функції. Завдання 6
# Виконала: Іващук Евеліна

# Завдання 6. Скласти програму для знаходження чисел з інтервалу [M, N],
# що мають найбільшу кількість дільників.


def find_max_divisors(m, n):
    # Функція повертає список чисел з інтервалу [m, n], що мають найбільшу
    # кількість дільників, і саму цю кількість.

    # counts[i] - кількість дільників числа m + i; спочатку всі лічильники рівні 0
    counts = [0] * (n - m + 1)

    # Для кожного можливого дільника d збільшуємо лічильник усіх чисел
    # інтервалу, які на нього діляться: це числа first, first + d, first + 2d, ...
    for d in range(1, n + 1):
        first = ((m + d - 1) // d) * d    # найменше число, не менше за m, кратне d
        for number in range(first, n + 1, d):
            counts[number - m] += 1

    max_count = max(counts)    # найбільша кількість дільників

    # Збираємо всі числа, у яких кількість дільників дорівнює найбільшій
    result = []
    for i in range(len(counts)):
        if counts[i] == max_count:
            result.append(m + i)

    return result, max_count


# Вводимо межі інтервалу
m = int(input("Enter M: "))
n = int(input("Enter N: "))

if 1 <= m <= n:
    # Функція повертає два значення, тому записуємо їх у дві змінні
    numbers, max_count = find_max_divisors(m, n)
    print("Numbers with the largest number of divisors:", numbers)
    print("Number of divisors:", max_count)
else:
    print("Error: the condition 1 <= M <= N must be met")
