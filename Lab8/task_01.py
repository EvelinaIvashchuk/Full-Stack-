# Лабораторна робота №8. Класи. Частина 3. Завдання 1
# Виконала: Іващук Евеліна

# Завдання 1. Створіть клас Alphabet зі статичними атрибутами lang і letters
# для української мови та методами print_alphabet(), letters_num(),
# is_ua_lang(). Створіть клас EngAlphabet шляхом успадкування від класу
# Alphabet: з приватним статичним атрибутом __en_letters_num, методом
# is_en_letter(), перевизначеним методом letters_num() і статичним методом
# example().


class Alphabet:
    # Статичні атрибути (атрибути класу) зі значеннями для української мови
    lang = "Ua"
    letters = list("абвгґдеєжзиіїйклмнопрстуфхцчшщьюя")

    def __init__(self, lang=None, letters=None):
        # Якщо мову або літери не передано, беремо значення за замовчуванням
        # зі статичних атрибутів класу
        if lang is None:
            lang = Alphabet.lang
        if letters is None:
            letters = Alphabet.letters
        self.lang = lang
        self.letters = letters

    def print_alphabet(self):
        # Метод виводить літери алфавіту в один рядок
        print(" ".join(self.letters))

    def letters_num(self):
        # Метод повертає кількість літер в алфавіті
        return len(self.letters)

    def is_ua_lang(self, text):
        # Метод визначає, чи відноситься текст до української мови незалежно
        # від регістру: усі літери тексту мають входити до українського алфавіту.
        # Пробіли, цифри та розділові знаки не враховуються.
        for char in text.lower():
            if char.isalpha() and char not in Alphabet.letters:
                return False
        return True


class EngAlphabet(Alphabet):
    # Приватний статичний атрибут: кількість літер в англійському алфавіті
    __en_letters_num = 26

    def __init__(self):
        # Викликаємо батьківський метод __init__() і передаємо йому
        # позначення мови та рядок з усіх літер алфавіту
        super().__init__("En", "abcdefghijklmnopqrstuvwxyz")

    def is_en_letter(self, letter):
        # Метод визначає, чи відноситься рядок до англійського алфавіту
        return letter.lower() in self.letters

    def letters_num(self):
        # Перевизначений метод: повертає значення приватного атрибута
        return EngAlphabet.__en_letters_num

    @staticmethod
    def example():
        # Статичний метод не отримує параметра self і не залежить від
        # конкретного об'єкта; його можна викликати через назву класу
        return "The quick brown fox jumps over the lazy dog."


# ---------- Тести до модуля ----------

# Створюємо об'єкт класу EngAlphabet
eng_alphabet = EngAlphabet()

# Друкуємо літери алфавіту для цього об'єкта
print("Letters of the alphabet:")
eng_alphabet.print_alphabet()

# Виводимо кількість літер в алфавіті
print("Number of letters:", eng_alphabet.letters_num())

# Перевіряємо, чи відноситься літера J до англійського алфавіту
print("Is J an English letter:", eng_alphabet.is_en_letter("J"))

# Перевіряємо, чи відноситься літера Щ до українського алфавіту
print("Is Щ a Ukrainian letter:", eng_alphabet.is_ua_lang("Щ"))

# Виводимо приклад тексту англійською мовою
print("Example:", EngAlphabet.example())
