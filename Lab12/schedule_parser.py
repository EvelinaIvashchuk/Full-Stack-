# Лабораторна робота №12. Парсинг сайтів
# Виконала: Іващук Евеліна

# Модуль schedule_parser отримує розклад занять денної форми з сайту
# Навчально-наукового інституту фізико-технічних та комп'ютерних наук ЧНУ
# і готує його для аналізу в завданнях 1-3.

import json    # розбір даних у форматі JSON
import os      # робота з файлами
import re      # регулярні вирази для пошуку в тексті
from urllib.parse import urljoin    # побудова повної адреси з відносної

import requests                  # завантаження сторінок
from bs4 import BeautifulSoup    # розбір HTML-коду сторінок

# Адреса сайту розкладу занять інституту. Посилання на нього розміщено на
# сайті інституту ptcsi.chnu.edu.ua в розділі "Студенту" - "Розклад занять".
SCHEDULE_URL = "https://shpatar26121974.github.io/nniftcn_schedule/"

# Файл, у який зберігається завантажений розклад, щоб не звертатися
# до сайту під час кожного запуску програми
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(BASE_DIR, "schedule.json")


def get_page(url):
    # Функція завантажує сторінку за адресою url і повертає її текст
    response = requests.get(url, timeout=30)
    response.raise_for_status()      # якщо сервер повернув помилку, буде виняток
    response.encoding = "utf-8"      # текст сторінок закодовано в UTF-8
    return response.text


def find_script_url():
    # Сайт розкладу - це вебзастосунок: його HTML-сторінка майже порожня,
    # а всі дані містяться у файлі JavaScript, який підключено тегом <script>.
    # Функція розбирає HTML-код сторінки і знаходить адресу цього файла.
    soup = BeautifulSoup(get_page(SCHEDULE_URL), "html.parser")

    # title - тег із назвою сторінки; виводимо її для перевірки
    print("Page title:", soup.title.get_text(strip=True))

    # find() шукає перший тег <script>, який має атрибут src
    script = soup.find("script", src=True)
    if script is None:
        raise ValueError("the script with the schedule is not found")

    # У src записано відносну адресу, urljoin() перетворює її на повну
    return urljoin(SCHEDULE_URL, script["src"])


def unescape(text):
    # У коді JavaScript текст записано зі службовими послідовностями:
    # А - код символу, \' - апостроф, \\ - зворотна коса риска.
    # Функція замінює їх звичайними символами.
    def replace(match):
        value = match.group(1)
        if value.startswith("u"):
            return chr(int(value[1:], 16))    # символ за його кодом
        return value

    return re.sub(r"\\(u[0-9a-fA-F]{4}|.)", replace, text)


def download_schedule():
    # Функція завантажує розклад із сайту і повертає список занять
    script_url = find_script_url()
    code = get_page(script_url)

    # Розклад записано в коді у вигляді JSON.parse('[...]').
    # Регулярний вираз знаходить текст між апострофами.
    match = re.search(r"JSON\.parse\('((?:[^'\\]|\\.)*)'\)", code)
    if match is None:
        raise ValueError("the schedule data is not found in the script")

    # Перетворюємо текст у список словників
    lessons = json.loads(unescape(match.group(1)))
    return lessons


def load_schedule():
    # Функція повертає список занять. Якщо розклад уже завантажували,
    # він читається з файла schedule.json, інакше завантажується із сайту.
    # Щоб оновити дані, досить видалити файл schedule.json.
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as file:
            lessons = json.load(file)
        print("Schedule is read from the file schedule.json:", len(lessons), "records")
    else:
        lessons = download_schedule()
        with open(CACHE_FILE, "w", encoding="utf-8") as file:
            json.dump(lessons, file, ensure_ascii=False, indent=1)
        print("Schedule is downloaded from", SCHEDULE_URL)
        print("Number of records:", len(lessons))
    return lessons


def get_rooms(text):
    # На сайті аудиторії записано по-різному: "8-326", "8-224*",
    # "8-116 // 8-106", "Корпус 8, ауд. 102Ц", "к.8,а.117".
    # Функція повертає список аудиторій у єдиному вигляді "корпус-аудиторія".
    rooms = []
    # Кілька аудиторій в одному записі розділено знаками "//"
    for part in text.replace("*", "").split("//"):
        part = part.strip()

        # Короткий запис: "8-326"
        match = re.match(r"^(\d+)-(\w+)$", part)
        if match is None:
            # Довгий запис: "Корпус 8, ауд. 102Ц" або "к.8,а.117"
            pattern = r"(?:[Кк]орпус|к\.)\s*(\d+)\s*[,.]?\s*(?:ауд|лаб|а)\.?\s*(\w+)"
            match = re.search(pattern, part)

        if match is not None:
            rooms.append(match.group(1) + "-" + match.group(2))
    return rooms


def get_busy_slots(lessons):
    # Функція повертає словник: аудиторія -> множина зайнятих "вікон" розкладу.
    # Вікно - це трійка (день, номер пари, номер тижня). Якщо на одній парі
    # в аудиторії сидять кілька груп (наприклад, на лекції), це одне заняття,
    # тому множина зберігає таке вікно лише один раз.
    busy = {}
    for lesson in lessons:
        slot = (lesson["day"], lesson["period"], lesson["week"])
        for room in get_rooms(lesson["room"]):
            if room not in busy:
                busy[room] = set()
            busy[room].add(slot)
    return busy


# Якщо модуль запущено як програму, показуємо кілька завантажених записів
if __name__ == "__main__":
    lessons = load_schedule()
    for lesson in lessons[:3]:
        print(lesson)
