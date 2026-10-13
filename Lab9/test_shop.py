# Лабораторна робота №9. Unit-тестування в мові Python
# Виконала: Іващук Евеліна

# Тести для класів Shop і Discount (модуль shop.py), написані за допомогою
# фреймворку unittest зі стандартної бібліотеки Python.

import contextlib    # засоби для тимчасового перенаправлення виводу
import io            # клас StringIO - "файл" у пам'яті, в який можна писати текст
import unittest      # фреймворк для unit-тестування

from shop import Shop, Discount    # класи, які тестуємо


def get_output(function):
    # Допоміжна функція: викликає передану функцію і повертає текст,
    # який вона вивела на екран функцією print()
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        function()
    return buffer.getvalue()


# Набір тестів - це клас, що успадковує від unittest.TestCase.
# Кожен метод, назва якого починається з test_, є окремим тестом.
class TestShop(unittest.TestCase):

    def setUp(self):
        # Метод setUp виконується перед кожним тестом:
        # створюємо новий магазин, щоб тести не впливали один на одного
        self.store = Shop("BookLand", "books")

    def test_attributes(self):
        # Конструктор має зберегти назву і тип магазину в атрибутах
        self.assertEqual(self.store.shop_name, "BookLand")
        self.assertEqual(self.store.store_type, "books")

    def test_default_number_of_units(self):
        # Кількість видів товару за замовчуванням дорівнює 0
        self.assertEqual(self.store.number_of_units, 0)

    def test_describe_shop(self):
        # Метод describe_shop() має вивести назву і тип магазину
        output = get_output(self.store.describe_shop)
        self.assertIn("BookLand", output)
        self.assertIn("books", output)

    def test_open_shop(self):
        # Метод open_shop() має вивести повідомлення, що магазин відкритий
        output = get_output(self.store.open_shop)
        self.assertIn("BookLand", output)
        self.assertIn("open", output)

    def test_change_number_of_units_directly(self):
        # Атрибут number_of_units можна змінити напряму
        self.store.number_of_units = 120
        self.assertEqual(self.store.number_of_units, 120)

    def test_set_number_of_units(self):
        # Метод set_number_of_units() задає кількість видів товару
        self.store.set_number_of_units(200)
        self.assertEqual(self.store.number_of_units, 200)

    def test_set_number_of_units_negative(self):
        # Кількість видів товару не може бути від'ємною: очікуємо виняток
        # ValueError, а значення атрибута має залишитися без змін
        with self.assertRaises(ValueError):
            self.store.set_number_of_units(-5)
        self.assertEqual(self.store.number_of_units, 0)

    def test_increment_number_of_units(self):
        # Метод increment_number_of_units() збільшує кількість на задану величину
        self.store.set_number_of_units(200)
        self.store.increment_number_of_units(50)
        self.assertEqual(self.store.number_of_units, 250)

    def test_increment_several_times(self):
        # Кілька викликів методу мають накопичувати значення
        self.store.increment_number_of_units(10)
        self.store.increment_number_of_units(15)
        self.assertEqual(self.store.number_of_units, 25)

    def test_increment_negative(self):
        # Метод призначений для збільшення, тому від'ємна величина - помилка
        self.store.set_number_of_units(100)
        with self.assertRaises(ValueError):
            self.store.increment_number_of_units(-30)
        self.assertEqual(self.store.number_of_units, 100)

    def test_instances_are_independent(self):
        # Зміна одного екземпляра не повинна впливати на інший
        other = Shop("TechnoWorld", "electronics")
        self.store.set_number_of_units(10)
        self.assertEqual(other.number_of_units, 0)
        self.assertEqual(other.shop_name, "TechnoWorld")


class TestDiscount(unittest.TestCase):

    def setUp(self):
        self.store_discount = Discount("BookLand", "books", ["novels", "comics"])

    def test_is_shop(self):
        # Клас Discount успадковує від Shop, тому його екземпляр є і екземпляром Shop
        self.assertIsInstance(self.store_discount, Shop)

    def test_inherited_attributes(self):
        # Атрибути батьківського класу мають бути створені конструктором
        self.assertEqual(self.store_discount.shop_name, "BookLand")
        self.assertEqual(self.store_discount.store_type, "books")
        self.assertEqual(self.store_discount.number_of_units, 0)

    def test_inherited_methods(self):
        # Методи батьківського класу мають працювати і для класу-нащадка
        self.store_discount.set_number_of_units(40)
        self.store_discount.increment_number_of_units(2)
        self.assertEqual(self.store_discount.number_of_units, 42)

    def test_discount_products(self):
        # Список товарів зі знижкою зберігається в атрибуті discount_products
        self.assertEqual(self.store_discount.discount_products, ["novels", "comics"])

    def test_get_discounts_products(self):
        # Метод має вивести всі товари зі знижкою
        output = get_output(self.store_discount.get_discounts_products)
        self.assertIn("novels", output)
        self.assertIn("comics", output)

    def test_default_discount_products(self):
        # Магазин можна створити без товарів зі знижкою: список має бути порожнім
        store = Discount("GreenGarden", "plants")
        self.assertEqual(store.discount_products, [])


# Якщо файл запущено як програму, запускаємо всі тести.
# verbosity=2 означає докладний вивід: назва і результат кожного тесту.
if __name__ == "__main__":
    unittest.main(verbosity=2)
