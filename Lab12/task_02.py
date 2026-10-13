# Лабораторна робота №12. Парсинг сайтів. Завдання 2
# Виконала: Іващук Евеліна

# Завдання 2. Визначте, які аудиторії з комп'ютерною технікою частіше всього
# залишаються не задіяними.

from schedule_parser import load_schedule, get_rooms, get_busy_slots

BUILDING = "8"    # аудиторії з комп'ютерною технікою шукаємо у 8 корпусі

# На сайті розкладу не вказано, в яких аудиторіях є комп'ютери.
# Якщо список таких аудиторій відомий, його можна записати сюди,
# наприклад: COMPUTER_ROOMS = ["8-114", "8-207", "8-209"]
COMPUTER_ROOMS = []

# Якщо список порожній, комп'ютерні аудиторії визначаються за розкладом:
# це аудиторії, де проводиться не менше MIN_LESSONS практичних чи лабораторних
# занять з дисциплін, назви яких містять одне з ключових слів.
KEYWORDS = ["програм", "алгоритм", "web", "баз", "скбд", "java", "мереж", "дизайн",
            ".net", "linux", "android", "devops", "тестуван", "аналіз даних",
            "штучн", "машинне навчання", "розробк", "cisco", "seo", "моделюван"]
MIN_LESSONS = 5

# Кількість "вікон" у розкладі за два тижні: 5 днів * 6 пар * 2 тижні
TOTAL_SLOTS = 5 * 6 * 2

lessons = load_schedule()
busy = get_busy_slots(lessons)

if len(COMPUTER_ROOMS) == 0:
    # Рахуємо для кожної аудиторії кількість "комп'ютерних" занять
    computer_lessons = {}
    for lesson in lessons:
        if lesson["type"] == "lecture":
            continue    # лекції не враховуємо
        subject = lesson["subject"].lower()
        is_computer = False
        for keyword in KEYWORDS:
            if keyword in subject:
                is_computer = True
        if is_computer:
            for room in get_rooms(lesson["room"]):
                if room.startswith(BUILDING + "-"):
                    computer_lessons[room] = computer_lessons.get(room, 0) + 1

    for room in computer_lessons:
        if computer_lessons[room] >= MIN_LESSONS:
            COMPUTER_ROOMS.append(room)

# Для кожної комп'ютерної аудиторії рахуємо вільні пари.
# Пари після шостої не враховуємо, бо занять на них майже немає.
rooms = []
for room in COMPUTER_ROOMS:
    occupied = 0
    for day, period, week in busy.get(room, set()):
        if period <= 6:
            occupied += 1
    free = TOTAL_SLOTS - occupied
    rooms.append([free, room, occupied])

# Сортуємо за кількістю вільних пар від найбільшої
rooms.sort(reverse=True)

print()
print("Rooms with computers in building", BUILDING + ":", len(rooms))
print("Room - free classes - busy classes - share of free time")
for free, room, occupied in rooms:
    percent = round(free / TOTAL_SLOTS * 100)
    print(room, "-", free, "-", occupied, "-", str(percent) + "%")

print()
print("Most often unused:", rooms[0][1], "-", rooms[0][0],
      "free classes out of", TOTAL_SLOTS)
