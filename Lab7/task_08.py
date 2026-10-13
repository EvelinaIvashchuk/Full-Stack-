# Лабораторна робота №7. Класи. Частина 2. Завдання 8
# Виконала: Іващук Евеліна

# Завдання 8. Онлайн-магазин. Класи Shop і Discount збережено в модулі
# shop.py, а ця програма імпортує їх і по черзі виконує пункти a-f завдання.

# Пункт f: імпортуємо класи з модуля shop (файл shop.py у цій самій папці)
from shop import Shop, Discount

# a. Створюємо екземпляр з ім'ям store, виводимо два атрибути окремо,
# потім викликаємо обидва методи
print("--- a ---")
store = Shop("BookLand", "books")
print(store.shop_name)
print(store.store_type)
store.describe_shop()
store.open_shop()

# b. Створюємо три різних екземпляри і для кожного викликаємо describe_shop()
print("--- b ---")
shop1 = Shop("TechnoWorld", "electronics")
shop2 = Shop("GreenGarden", "plants")
shop3 = Shop("SportLife", "sports goods")
shop1.describe_shop()
shop2.describe_shop()
shop3.describe_shop()

# c. Виводимо значення number_of_units (за замовчуванням 0),
# змінюємо атрибут напряму і виводимо знову
print("--- c ---")
store = Shop("BookLand", "books")
print("Number of units:", store.number_of_units)
store.number_of_units = 120
print("Number of units:", store.number_of_units)

# d. Задаємо кількість видів товару методом set_number_of_units(),
# потім збільшуємо її методом increment_number_of_units()
print("--- d ---")
store.set_number_of_units(200)
print("Number of units:", store.number_of_units)
store.increment_number_of_units(50)
print("Number of units:", store.number_of_units)

# e. Створюємо екземпляр класу Discount, що успадковує від Shop,
# і виводимо список товарів зі знижкою
print("--- e ---")
store_discount = Discount("BookLand", "books", ["novels", "dictionaries", "comics"])
store_discount.describe_shop()    # метод, успадкований від класу Shop
store_discount.get_discounts_products()

# f. Створюємо екземпляр all_store і викликаємо один з методів класу Shop,
# щоб перевірити, що імпорт працює правильно
print("--- f ---")
all_store = Shop("AllStore", "supermarket")
all_store.open_shop()
