# Лабораторна робота №7. Класи. Частина 2. Завдання 1
# Виконала: Іващук Евеліна

# Завдання 1. Напишіть клас Bank для опису простих операцій з вашим
# банківським рахунком: покласти на рахунок, зняти з рахунку, переглянути
# рахунок. При створенні екземпляру класу екземпляр отримує атрибут __balance
# з певним значенням. Клас повинен містити методи для додавання коштів на
# рахунок і знімання з рахунку, за умови, що на рахунку достатньо коштів.


class Bank:
    # Клас описує банківський рахунок

    def __init__(self, balance):
        # Два підкреслення на початку назви роблять атрибут прихованим (приватним):
        # до нього можна звертатися тільки всередині методів класу
        self.__balance = balance

    def deposit(self, amount):
        # Метод додає кошти на рахунок; сума має бути додатною
        if amount > 0:
            self.__balance += amount
            print("Deposited:", amount)
        else:
            print("Error: the amount must be positive")

    def withdraw(self, amount):
        # Метод знімає кошти з рахунку, якщо на рахунку достатньо коштів
        if amount <= 0:
            print("Error: the amount must be positive")
        elif amount <= self.__balance:
            self.__balance -= amount
            print("Withdrawn:", amount)
        else:
            print("Error: insufficient funds to withdraw", amount)

    def get_balance(self):
        # Метод повертає поточний стан рахунку
        return self.__balance


# Створюємо рахунок з початковим балансом 1000
account = Bank(1000)
print("Balance:", account.get_balance())

# Кладемо кошти на рахунок
account.deposit(500)
print("Balance:", account.get_balance())

# Знімаємо кошти з рахунку
account.withdraw(300)
print("Balance:", account.get_balance())

# Пробуємо зняти більше, ніж є на рахунку
account.withdraw(5000)
print("Balance:", account.get_balance())

# Перевіряємо, що прихований атрибут недоступний ззовні класу
try:
    print(account.__balance)
except AttributeError:
    print("The attribute __balance is not accessible outside the class")
