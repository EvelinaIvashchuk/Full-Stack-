# Лабораторна робота №5. Робота з файлами. Завдання 7
# Виконала: Іващук Евеліна

# Завдання 7. Завантажте файл marks.csv і визначте кількість студентів, що
# проходили тестування. Виведіть інформацію про те, яку оцінку набрали
# відповідна кількість студентів. Виведіть інформацію, яку середню оцінку
# отримував студент за певний час виконання КМР (крок - 1 хв). Створіть
# текстовий файл і запишіть в нього статистику по правильним відповідям для
# кожного окремого питання (який відсоток правильних і неправильних
# відповідей на питання дали студенти). В цей же файл внесіть інформацію про
# 5 найкращих оцінок в співвідношенні оцінка/час, витрачений на складання КМР.

import csv    # модуль для читання файлів у форматі CSV
import os     # модуль для роботи з файловою системою

# Робимо поточним каталог, у якому лежить програма
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def to_number(value):
    # У файлі дробові числа записані через кому ("8,50"), а Python розуміє
    # тільки крапку, тому перед перетворенням замінюємо кому на крапку
    return float(value.replace(",", "."))


# Читаємо файл. Кожен рядок файла - результат одного студента:
# [0] код студента, [1] початок, [2] завершення, [3] витрачений час,
# [4] оцінка, [5:] бали за кожне питання
rows = []
with open("marks.csv", "r", encoding="utf-8") as file:
    # csv.reader розбиває кожен рядок файла на список значень
    for row in csv.reader(file):
        rows.append(row)

students = len(rows)
questions = len(rows[0]) - 5    # кількість питань у тесті

print("Number of students:", students)

marks_count = {}        # словник: оцінка -> кількість студентів
marks_by_minute = {}    # словник: кількість хвилин -> список оцінок
correct = [0] * questions    # кількість правильних відповідей на кожне питання
ratios = []             # список [оцінка / час, оцінка, час у хвилинах, код студента]

for row in rows:
    mark = to_number(row[4])

    # Рахуємо, скільки студентів отримали таку оцінку
    if mark in marks_count:
        marks_count[mark] += 1
    else:
        marks_count[mark] = 1

    # Час записано як "15 хв 17 сек" або "20 хв": розбиваємо рядок на частини
    parts = row[3].split()
    minutes = int(parts[0])
    seconds = 0
    if len(parts) == 4:
        seconds = int(parts[2])

    # Додаємо оцінку до списку оцінок для цієї кількості хвилин
    if minutes not in marks_by_minute:
        marks_by_minute[minutes] = []
    marks_by_minute[minutes].append(mark)

    # Співвідношення оцінка / час (час у хвилинах з урахуванням секунд)
    total_minutes = minutes + seconds / 60
    ratios.append([mark / total_minutes, mark, round(total_minutes, 2), row[0]])

    # Відповідь правильна, якщо за питання отримано більше 0 балів.
    # Прочерк "-" означає, що відповіді немає - вважаємо її неправильною.
    for i in range(questions):
        value = row[5 + i]
        if value != "-" and to_number(value) > 0:
            correct[i] += 1

# Виводимо, скільки студентів отримали кожну оцінку (оцінки за зростанням)
print()
print("Mark - number of students:")
for mark in sorted(marks_count):
    print(mark, "-", marks_count[mark])

# Виводимо середню оцінку для кожного часу виконання з кроком 1 хвилина
print()
print("Time (minutes) - average mark:")
for minutes in sorted(marks_by_minute):
    marks = marks_by_minute[minutes]
    average = sum(marks) / len(marks)
    print(minutes, "-", round(average, 2))

# Сортуємо список за першим елементом (оцінка / час) від найбільшого
ratios.sort(reverse=True)

# Записуємо статистику в текстовий файл
with open("marks_statistics.txt", "w", encoding="utf-8") as file:
    file.write("Statistics of answers for each question\n")
    file.write("Question - correct, % - incorrect, %\n")
    for i in range(questions):
        percent = correct[i] / students * 100
        line = str(i + 1) + " - " + str(round(percent, 2)) + " - "
        line += str(round(100 - percent, 2))
        file.write(line + "\n")

    file.write("\n")
    file.write("5 best results by the ratio mark / time\n")
    file.write("Mark - time, minutes - ratio - student\n")
    for item in ratios[:5]:
        line = str(item[1]) + " - " + str(item[2]) + " - "
        line += str(round(item[0], 3)) + " - " + item[3]
        file.write(line + "\n")

print()
print("The statistics are saved to the file marks_statistics.txt")
