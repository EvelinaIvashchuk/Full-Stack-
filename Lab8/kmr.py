# Лабораторна робота №8. Класи. Частина 3. Завдання 4
# Виконала: Іващук Евеліна

# Модуль kmr містить класи для аналізу результатів КМР (контрольних
# модульних робіт) з CSV-файлів: KmrCsv читає файл, Statistic рахує
# статистику, Plots будує графіки, а KmrWork успадковує всі три класи одразу
# (множинне наслідування).

import csv    # читання файлів у форматі CSV
import os     # робота з файлами і каталогами

import matplotlib.pyplot as plt    # побудова графіків

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class KmrCsv:
    # Атрибути класу за замовчуванням
    ref = "kmr1.csv"    # посилання на CSV-файл з оцінками
    num = 1             # номер КМР

    def set_ref(self, ref):
        # Встановлює посилання на файл з оцінками
        self.ref = ref

    def get_ref(self):
        # Повертає посилання на файл з оцінками
        return self.ref

    def set_num(self, num):
        # Встановлює номер КМР
        self.num = num

    def read(self):
        # Читає файл з оцінками і повертає список рядків. Кожен рядок - результат
        # одного студента: [0] id студента, [1] початок, [2] завершення,
        # [3] витрачений час, [4] підсумкова оцінка, [5:] бали за питання.
        rows = []
        with open(os.path.join(BASE_DIR, self.ref), "r", encoding="utf-8") as file:
            for row in csv.reader(file):
                rows.append(row)
        return rows

    def info(self):
        # Виводить інформацію про файл: номер КМР і кількість студентів
        print("KMR", self.num, "- file", self.ref, "- students:", len(self.read()))


class Statistic:
    # Клас-міксин: сам не зберігає даних, а додає методи статистики класу,
    # який має метод read()

    @staticmethod
    def to_number(value):
        # У файлі дробові числа записано через кому, а прочерк означає
        # відсутність відповіді
        if value == "-":
            return 0.0
        return float(value.replace(",", "."))

    @staticmethod
    def to_minutes(value):
        # Перетворює час виду "15 хв 17 сек" або "20 хв" на кількість хвилин
        parts = value.split()
        minutes = int(parts[0])
        if len(parts) == 4:
            minutes += int(parts[2]) / 60
        return minutes

    def avg_stat(self):
        # Визначає відсоток правильних відповідей на кожне питання серед усіх
        # студентів і повертає результат у вигляді кортежу чисел
        rows = self.read()
        result = []
        for column in range(5, len(rows[0])):
            scores = []
            for row in rows:
                scores.append(self.to_number(row[column]))
            # Відповідь правильна, якщо за питання отримано найбільший бал
            correct = scores.count(max(scores))
            result.append(round(correct / len(rows) * 100, 2))
        return tuple(result)

    def marks_stat(self):
        # Визначає, яку оцінку набрала яка кількість студентів.
        # Повертає словник {оцінка: кількість студентів}.
        counts = {}
        for row in self.read():
            mark = self.to_number(row[4])
            counts[mark] = counts.get(mark, 0) + 1
        # Повертаємо словник, упорядкований за зростанням оцінки
        result = {}
        for mark in sorted(counts):
            result[mark] = counts[mark]
        return result

    def marks_per_time(self):
        # Визначає, який середній бал за хвилину набирав кожен студент.
        # Повертає словник {id студента: середній бал за хвилину}.
        result = {}
        for row in self.read():
            mark = self.to_number(row[4])
            result[row[0]] = round(mark / self.to_minutes(row[3]), 3)
        return result

    def best_marks_per_time(self, bottom_margin, top_margin):
        # Для студентів з підсумковою оцінкою від bottom_margin до top_margin
        # формує п'ять найкращих результатів середнього бала за хвилину.
        # Повертає кортеж з кортежів (id студента, оцінка, бал за хвилину).
        per_time = self.marks_per_time()
        selected = []
        for row in self.read():
            mark = self.to_number(row[4])
            if bottom_margin <= mark <= top_margin:
                # Першим ставимо бал за хвилину, щоб сортувати за ним
                selected.append((per_time[row[0]], row[0], mark))
        selected.sort(reverse=True)

        result = []
        for speed, student, mark in selected[:5]:
            result.append((student, mark, speed))
        return tuple(result)


class Plots:
    # Клас-міксин: додає методи побудови графіків
    cat = "results"    # каталог, у який зберігаються графіки

    def set_cat(self, cat):
        # Встановлює каталог для збереження графіків і створює його
        self.cat = cat
        os.makedirs(os.path.join(BASE_DIR, cat), exist_ok=True)

    def save_plot(self, name):
        # Допоміжний метод: зберігає поточний графік у файл і закриває його
        path = os.path.join(BASE_DIR, self.cat, name)
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        print("Plot is saved:", os.path.join(self.cat, name))

    def avg_plot(self, avg):
        # Гістограма відсотків правильних відповідей на кожне питання
        questions = list(range(1, len(avg) + 1))
        plt.figure(figsize=(9, 4))
        plt.bar(questions, avg, color="steelblue")
        plt.title("KMR " + str(self.num) + ": correct answers for each question")
        plt.xlabel("Question")
        plt.ylabel("Correct answers, %")
        plt.xticks(questions)
        self.save_plot("kmr" + str(self.num) + "_avg.png")

    def marks_plot(self, marks):
        # Гістограма: скільки студентів набрали кожну оцінку
        labels = []
        for mark in marks:
            labels.append(str(mark))
        plt.figure(figsize=(9, 4))
        plt.bar(labels, list(marks.values()), color="seagreen")
        plt.title("KMR " + str(self.num) + ": number of students for each mark")
        plt.xlabel("Mark")
        plt.ylabel("Students")
        plt.xticks(rotation=45)
        self.save_plot("kmr" + str(self.num) + "_marks.png")

    def best_marks_plot(self, best):
        # Гістограма п'яти найкращих результатів середнього бала за хвилину
        labels = []
        speeds = []
        for student, mark, speed in best:
            # На графіку показуємо перші 6 символів id і підсумкову оцінку
            labels.append(student[:6] + "\n(mark " + str(mark) + ")")
            speeds.append(speed)
        plt.figure(figsize=(9, 4))
        plt.bar(labels, speeds, color="darkorange")
        plt.title("KMR " + str(self.num) + ": five best marks per minute")
        plt.xlabel("Student")
        plt.ylabel("Mark per minute")
        self.save_plot("kmr" + str(self.num) + "_best.png")


class KmrWork(KmrCsv, Statistic, Plots):
    # Клас успадковує одразу три класи і отримує методи кожного з них

    # Статичні атрибути
    kmrs = {}          # словник {номер КМР: адреса відповідного csv-файла}
    cat = "results"    # каталог для збереження результатів роботи

    def __init__(self, ref, num):
        self.set_ref(ref)
        self.set_num(num)
        self.set_cat(KmrWork.cat)
        # Запам'ятовуємо файл у спільному для всіх об'єктів словнику
        KmrWork.kmrs[num] = ref

    @classmethod
    def compare_csv(cls):
        # Метод класу (отримує сам клас у параметрі cls, а не об'єкт).
        # Виводить на екран і зберігає в txt-файл порівняння статистики КМР:
        # кількість виконаних КМР, середній бал і середній час виконання.
        lines = ["KMR - works done - average mark - average time, min"]
        for num in sorted(cls.kmrs):
            kmr = cls(cls.kmrs[num], num)
            rows = kmr.read()
            marks = []
            times = []
            for row in rows:
                marks.append(kmr.to_number(row[4]))
                times.append(kmr.to_minutes(row[3]))
            average_mark = round(sum(marks) / len(marks), 2)
            average_time = round(sum(times) / len(times), 2)
            lines.append(str(num) + " - " + str(len(rows)) + " - " + str(average_mark)
                         + " - " + str(average_time))

        for line in lines:
            print(line)
        path = os.path.join(BASE_DIR, cls.cat, "compare.txt")
        with open(path, "w", encoding="utf-8") as file:
            file.write("\n".join(lines) + "\n")
        print("Comparison is saved:", os.path.join(cls.cat, "compare.txt"))

    @classmethod
    def compare_avg_plots(cls):
        # Виводить на екран і зберігає гістограми з відсотками правильних
        # відповідей на кожне питання для всіх КМР (одна під одною)
        numbers = sorted(cls.kmrs)
        figure, axes = plt.subplots(len(numbers), 1, figsize=(9, 7))
        for i in range(len(numbers)):
            kmr = cls(cls.kmrs[numbers[i]], numbers[i])
            avg = kmr.avg_stat()
            questions = list(range(1, len(avg) + 1))
            axes[i].bar(questions, avg, color="steelblue")
            axes[i].set_title("KMR " + str(numbers[i]) + ": correct answers, %")
            axes[i].set_xticks(questions)
            axes[i].set_ylim(0, 100)
        path = os.path.join(BASE_DIR, cls.cat, "compare_avg.png")
        plt.tight_layout()
        plt.savefig(path)
        print("Plot is saved:", os.path.join(cls.cat, "compare_avg.png"))
        plt.show()    # показуємо графік у вікні
        plt.close()
