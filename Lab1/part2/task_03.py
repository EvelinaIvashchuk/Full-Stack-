# Лабораторна робота №1. Частина 2. Завдання 3
# Виконала: Іващук Евеліна

# Завдання 3. Написати програму обчислення вартості покупки з урахуванням
# знижки. Знижка в 3% надається в тому випадку, якщо сума покупки більше
# 500 грн., в 5% - якщо сума більше 1000 грн.

# Вводимо суму покупки (може бути дробовою, тому float)
total = float(input("Enter the purchase amount, UAH: "))

# Визначаємо відсоток знижки.
# Спочатку перевіряємо більшу суму, бо число, більше за 1000, також більше за 500.
if total > 1000:
    discount = 5      # знижка 5%
elif total > 500:
    discount = 3      # знижка 3%
else:
    discount = 0      # знижки немає

# Обчислюємо суму знижки та вартість покупки з її урахуванням
discount_sum = total * discount / 100
price = total - discount_sum

print("Discount:", discount, "%")
print("Discount amount:", round(discount_sum, 2), "UAH")
print("Price to pay:", round(price, 2), "UAH")
