# Лабораторна робота №5. Робота з файлами. Завдання 4
# Виконала: Іващук Евеліна

# Завдання 4. Прочитайте кожен рядок зі створеного у попередньому завданні
# файла learning_python.txt і замініть слово Python назвою іншої мови,
# наприклад C, при виведенні на екран. Отриманий файл має бути створений в
# новому каталозі, що розміщується в поточному. Відкрийте файл пострічково і
# дайте можливість користувачеві визначити, які змінені фрази є актуальними,
# наприклад для мови C, а які ні. Всі хибні твердження запишіть в інший
# файл, а істинні - в поточний.

import os    # модуль для роботи з файловою системою

# Робимо поточним каталог, у якому лежить програма
os.chdir(os.path.dirname(os.path.abspath(__file__)))

language = input("Enter the name of another language: ")

# Створюємо новий каталог у поточному. exist_ok=True означає:
# якщо каталог уже існує, помилки не буде.
directory = "other_language"
os.makedirs(directory, exist_ok=True)

# os.path.join() з'єднує назву каталогу і назву файла в один шлях
new_file = os.path.join(directory, "learning_language.txt")
false_file = os.path.join(directory, "false_statements.txt")

# Читаємо початковий файл, у кожному рядку замінюємо слово Python назвою
# іншої мови, виводимо рядок на екран і записуємо у новий файл
print("Changed text:")
with open("learning_python.txt", "r", encoding="utf-8") as source:
    with open(new_file, "w", encoding="utf-8") as target:
        for line in source:
            changed = line.strip().replace("Python", language)
            print(changed)
            target.write(changed + "\n")

true_lines = []     # істинні твердження
false_lines = []    # хибні твердження

# Відкриваємо новий файл пострічково і питаємо користувача про кожну фразу
print()
print("Is the statement true for", language, "? Enter y (yes) or n (no)")
with open(new_file, "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        answer = input(line + " ")
        if answer.lower() == "y":
            true_lines.append(line)
        else:
            false_lines.append(line)

# Істинні твердження записуємо в поточний (новий) файл, замінюючи його вміст
with open(new_file, "w", encoding="utf-8") as file:
    for line in true_lines:
        file.write(line + "\n")

# Хибні твердження записуємо в інший файл
with open(false_file, "w", encoding="utf-8") as file:
    for line in false_lines:
        file.write(line + "\n")

print()
print("True statements:", len(true_lines), "- saved to", new_file)
print("False statements:", len(false_lines), "- saved to", false_file)
