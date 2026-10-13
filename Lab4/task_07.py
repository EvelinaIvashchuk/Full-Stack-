# Лабораторна робота №4. Функції. Завдання 7
# Виконала: Іващук Евеліна

# Завдання 7. Написати функцію для пошуку всіх простих чисел від 0 до N з
# можливістю вибору формату представлення результату (списком; рядками в
# стовпчик; просто вивести кількість простих чисел).


def find_primes(n, mode):
    # Функція шукає всі прості числа від 0 до n методом "решето Ератосфена"
    # і виводить результат у вибраному форматі:
    # mode = 1 - списком, mode = 2 - в стовпчик, mode = 3 - лише кількість.

    # is_prime[i] дорівнює True, якщо число i вважається простим.
    # Спочатку вважаємо простими всі числа, крім 0 і 1.
    is_prime = [True] * (n + 1)
    is_prime[0] = False
    if n >= 1:
        is_prime[1] = False

    # Для кожного простого числа i викреслюємо всі числа, кратні йому.
    # Достатньо перевірити числа i, для яких i * i <= n.
    i = 2
    while i * i <= n:
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
        i += 1

    # Збираємо в список усі числа, які залишилися невикресленими
    primes = []
    for i in range(n + 1):
        if is_prime[i]:
            primes.append(i)

    # Виводимо результат у вибраному форматі
    if mode == 1:
        print(primes)
    elif mode == 2:
        for prime in primes:
            print(prime)
    else:
        print("Number of prime numbers:", len(primes))

    return primes


# Вводимо число N і формат представлення результату
n = int(input("Enter N: "))
print("Output format: 1 - list, 2 - column, 3 - only the number of primes")
mode = int(input("Choose the format: "))

if n >= 0 and 1 <= mode <= 3:
    find_primes(n, mode)
else:
    print("Error: N must not be negative, the format must be 1, 2 or 3")
