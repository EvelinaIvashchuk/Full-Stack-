# Лабораторна робота №12. Парсинг сайтів. Завдання 3
# Виконала: Іващук Евеліна

# Завдання 3. Визначте, в якій аудиторії частіше всього проходять заняття
# у вашої групи.

from schedule_parser import load_schedule, get_rooms

# Номер групи. На сайті група поділена на підгрупи "444(1)" і "444(2)",
# тому шукаємо всі записи, назва групи в яких починається з цього номера.
GROUP = "444"


def count_rooms(lessons, group_name):
    # Функція рахує, скільки занять проходить у кожній аудиторії для груп,
    # назва яких починається з group_name. Повертає список [кількість, аудиторія],
    # відсортований від найбільшої кількості.
    slots = {}    # аудиторія -> множина пар (день, номер пари, тиждень)
    for lesson in lessons:
        if lesson["group"].startswith(group_name):
            slot = (lesson["day"], lesson["period"], lesson["week"])
            for room in get_rooms(lesson["room"]):
                if room not in slots:
                    slots[room] = set()
                # Спільне заняття двох підгруп потрапляє в множину один раз
                slots[room].add(slot)

    rooms = []
    for room in slots:
        rooms.append([len(slots[room]), room])
    rooms.sort(reverse=True)
    return rooms


def best_rooms(rooms):
    # Функція повертає назви всіх аудиторій з найбільшою кількістю занять
    # (їх може бути кілька, якщо кількість однакова)
    names = []
    for count, room in rooms:
        if count == rooms[0][0]:
            names.append(room)
    names.sort()
    return ", ".join(names)


lessons = load_schedule()

# Назви підгруп, знайдені на сайті
subgroups = []
for lesson in lessons:
    name = lesson["group"]
    if name.startswith(GROUP) and name not in subgroups:
        subgroups.append(name)
subgroups.sort()

print()
print("Group", GROUP, "- subgroups on the site:", ", ".join(subgroups))

# Аудиторії всієї групи
rooms = count_rooms(lessons, GROUP)
print("Room - number of classes (per two weeks):")
for count, room in rooms:
    print(room, "-", count)

print()
print("Most often the classes of group", GROUP, "are held in", best_rooms(rooms),
      "-", rooms[0][0], "classes each")

# Те саме окремо для кожної підгрупи
for subgroup in subgroups:
    rooms = count_rooms(lessons, subgroup)
    print("Subgroup", subgroup, "- most often in", best_rooms(rooms),
          "-", rooms[0][0], "classes each")
