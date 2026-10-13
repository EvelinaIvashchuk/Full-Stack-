# Лабораторна робота №8. Класи. Частина 3. Завдання 2
# Виконала: Іващук Евеліна

# Завдання 2. Створіть клас Human зі статичними атрибутами default_name і
# default_age, публічними атрибутами name і age та приватними money і house,
# методами info(), default_info(), earn_money(), buy_house() і приватним
# методом make_deal(). Створіть клас House з атрибутами _area і _price та
# методом final_price(). Створіть клас SmallHouse, успадкований від House,
# який створює будинок площею 40 м2.


class House:
    def __init__(self, area=100, price=50000):
        # Одне підкреслення на початку назви означає захищений (protected)
        # атрибут: ним користуються сам клас і його нащадки
        self._area = area      # площа, м2
        self._price = price    # ціна

    def final_price(self, discount):
        # Метод повертає ціну з урахуванням знижки (у відсотках)
        return self._price * (100 - discount) / 100


class SmallHouse(House):
    def __init__(self, price=20000):
        # Перевизначений конструктор: площа маленького будинку завжди 40 м2
        super().__init__(40, price)


class Human:
    # Статичні атрибути зі значеннями за замовчуванням
    default_name = "No name"
    default_age = 0

    def __init__(self, name=default_name, age=default_age):
        self.name = name        # публічний атрибут
        self.age = age          # публічний атрибут
        self.__money = 0        # приватний атрибут: кількість грошей
        self.__house = None     # приватний атрибут: посилання на об'єкт House

    def info(self):
        # Метод виводить поля name, age, house і money
        print("Name:", self.name)
        print("Age:", self.age)
        if self.__house is None:
            print("House: no house")
        else:
            print("House: area", self.__house._area, "m2")
        print("Money:", self.__money)

    @staticmethod
    def default_info():
        # Довідковий статичний метод: виводить статичні поля класу
        print("Default name:", Human.default_name)
        print("Default age:", Human.default_age)

    def __make_deal(self, house, price):
        # Приватний метод - технічна реалізація покупки будинку:
        # зменшує кількість грошей і запам'ятовує куплений будинок
        self.__money -= price
        self.__house = house

    def earn_money(self, amount):
        # Метод збільшує кількість грошей
        self.__money += amount
        print("Earned", amount, "- now the money is", self.__money)

    def buy_house(self, house, discount=10):
        # Метод перевіряє, чи достатньо грошей для покупки будинку зі знижкою
        # (за замовчуванням 10%), і здійснює покупку
        price = house.final_price(discount)
        if self.__money >= price:
            self.__make_deal(house, price)
            print("The house is bought for", price)
        else:
            print("Warning: not enough money! The price is", price,
                  "but the money is only", self.__money)


# ---------- Тести до модуля ----------

# Викликаємо довідковий метод default_info() для класу Human
Human.default_info()
print()

# Створюємо об'єкт класу Human і виводимо довідкову інформацію про нього
human = Human("Olena", 25)
human.info()
print()

# Створюємо об'єкт класу SmallHouse
small_house = SmallHouse(20000)

# Пробуємо купити будинок: грошей ще немає, тому отримуємо попередження
human.buy_house(small_house)

# Виправляємо фінансове становище
human.earn_money(25000)

# Знову пробуємо купити будинок
human.buy_house(small_house)
print()

# Дивимося, як змінився стан об'єкта класу Human
human.info()
