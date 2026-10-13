# Лабораторна робота №7. Класи. Частина 2. Завдання 8
# Виконала: Іващук Евеліна

# Модуль shop містить класи Shop і Discount для завдання 8 "Онлайн-магазин"


class Shop:
    # Клас описує онлайн-магазин

    def __init__(self, shop_name, store_type):
        self.shop_name = shop_name      # назва магазину
        self.store_type = store_type    # тип магазину
        self.number_of_units = 0        # кількість видів товару, за замовчуванням 0

    def describe_shop(self):
        # Метод виводить назву і тип магазину
        print("Shop:", self.shop_name, "- type:", self.store_type)

    def open_shop(self):
        # Метод виводить повідомлення про те, що онлайн-магазин відкритий
        print("The online shop", self.shop_name, "is open")

    def set_number_of_units(self, number):
        # Метод задає кількість видів товару
        self.number_of_units = number

    def increment_number_of_units(self, amount):
        # Метод збільшує кількість видів товару на задану величину
        self.number_of_units += amount


class Discount(Shop):
    # Клас успадковує від класу Shop і додає список товарів зі знижкою

    def __init__(self, shop_name, store_type, discount_products):
        # super() звертається до батьківського класу: викликаємо його
        # конструктор, щоб створити атрибути, описані в класі Shop
        super().__init__(shop_name, store_type)
        self.discount_products = discount_products    # список товарів зі знижкою

    def get_discounts_products(self):
        # Метод виводить список товарів, на які встановлена знижка
        print("Discount products:", self.discount_products)
