# Лабораторна робота №7. Класи. Частина 2. Завдання 7
# Виконала: Іващук Евеліна

# Завдання 7. Напишіть один клас для перетворення десяткового числа на число
# в римській системі числення. І ще один клас для перетворення числа з
# римської системи числення у десяткове число.


class DecimalToRoman:
    # Клас перетворює десяткове число на число в римській системі числення

    # Значення і відповідні їм римські позначення в порядку зменшення.
    # Крім основних цифр, тут є пари, що записуються відніманням: 900 = CM, 4 = IV.
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    symbols = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]

    def convert(self, number):
        # Римськими цифрами записують числа від 1 до 3999
        if number < 1 or number > 3999:
            raise ValueError("the number must be from 1 to 3999")

        result = ""
        # Перебираємо значення від найбільшого: поки значення вміщується
        # в число, додаємо його позначення до результату і віднімаємо від числа
        for i in range(len(self.values)):
            while number >= self.values[i]:
                result += self.symbols[i]
                number -= self.values[i]
        return result


class RomanToDecimal:
    # Клас перетворює число з римської системи числення у десяткове число

    # Словник: римська цифра -> її значення
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

    def convert(self, roman):
        roman = roman.upper()    # дозволяємо вводити і малі літери
        result = 0

        for i in range(len(roman)):
            if roman[i] not in self.values:
                raise ValueError("'" + roman[i] + "' is not a Roman numeral")
            value = self.values[roman[i]]

            # Якщо після цифри стоїть більша цифра (наприклад, IV або XC),
            # значення цифри віднімаємо, інакше додаємо
            if i + 1 < len(roman) and value < self.values.get(roman[i + 1], 0):
                result -= value
            else:
                result += value
        return result


# Перетворення десяткового числа на римське
number = int(input("Enter a decimal number (1-3999): "))
print("Roman number:", DecimalToRoman().convert(number))

# Перетворення римського числа на десяткове
roman = input("Enter a Roman number: ")
print("Decimal number:", RomanToDecimal().convert(roman))
