# Лабораторна робота №8. Класи. Частина 3. Завдання 4
# Виконала: Іващук Евеліна

# Завдання 4. Створіть класи KmrCsv, Statistic і Plots та клас KmrWork, що
# успадковує всі три. Класи збережено в модулі kmr.py, а ця програма виконує
# тести до модуля.

from kmr import KmrWork

# Створюємо об'єкти kmr1 і kmr2 класу KmrWork: посилання на csv-файл і номер КМР
kmr1 = KmrWork("kmr1.csv", 1)
kmr2 = KmrWork("kmr2.csv", 2)

# Інформація про файли (метод успадковано від класу KmrCsv)
kmr1.info()
kmr2.info()
print("KMR files:", KmrWork.kmrs)
print()

# Порядок пошуку методів при множинному наслідуванні (MRO)
names = []
for cls in KmrWork.__mro__:
    names.append(cls.__name__)
print("Method resolution order:", " -> ".join(names))
print()

# Для об'єкта kmr2 використовуємо методи avg_plot() і marks_plot().
# Дані для графіків повертають методи, успадковані від класу Statistic.
avg = kmr2.avg_stat()
print("Correct answers for each question, %:")
print(avg)
kmr2.avg_plot(avg)
print()

marks = kmr2.marks_stat()
print("Mark: number of students")
print(marks)
kmr2.marks_plot(marks)
print()

# П'ять найкращих результатів бала за хвилину серед оцінок від 8 до 10
best = kmr2.best_marks_per_time(8, 10)
print("Five best marks per minute (student id, mark, mark per minute):")
for item in best:
    print(item)
kmr2.best_marks_plot(best)
print()

# Для класу KmrWork використовуємо методи compare_csv() і compare_avg_plots()
KmrWork.compare_csv()
KmrWork.compare_avg_plots()
