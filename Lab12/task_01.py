# Лабораторна робота №12. Парсинг сайтів. Завдання 1
# Виконала: Іващук Евеліна

# Завдання 1. Визначте, в яких аудиторіях проводиться більше всього занять
# у 8 корпусі ЧНУ серед усіх груп і усіх курсів.

from schedule_parser import load_schedule, get_busy_slots

BUILDING = "8"    # номер корпусу

# Завантажуємо розклад і рахуємо зайняті пари для кожної аудиторії
lessons = load_schedule()
busy = get_busy_slots(lessons)

# Відбираємо аудиторії 8 корпусу: їх назви починаються з "8-".
# Для кожної аудиторії зберігаємо пару [кількість занять, назва].
rooms = []
for room in busy:
    if room.startswith(BUILDING + "-"):
        rooms.append([len(busy[room]), room])

# Сортуємо за кількістю занять від найбільшої
rooms.sort(reverse=True)

print()
print("Rooms of building", BUILDING, "in the schedule:", len(rooms))
print("Top 10 rooms by the number of classes (per two weeks):")
for count, room in rooms[:10]:
    print(room, "-", count)

# Найбільша кількість занять і всі аудиторії, де вона досягається
max_count = rooms[0][0]
best = []
for count, room in rooms:
    if count == max_count:
        best.append(room)

print()
print("Most classes are held in:", ", ".join(best), "-", max_count, "classes")
