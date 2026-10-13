# Лабораторна робота №11. Telegram-бот
# Виконала: Іващук Евеліна

# Telegram-бот для тестування знань мови Python. Після команди /start бот
# по черзі задає 10 питань з чотирма варіантами відповіді у вигляді кнопок,
# після кожної відповіді повідомляє, чи вона правильна, а в кінці показує
# кількість набраних балів, дату і тривалість проходження тесту.

import os        # доступ до змінних середовища і файлів
import random    # випадковий порядок питань і відповідей
import sys       # завершення програми, якщо немає токена
from datetime import datetime    # дата, час і тривалість тесту

import telebot                # бібліотека pyTelegramBotAPI
from telebot import types     # кнопки та інші об'єкти Telegram

from questions import QUESTIONS    # список тестових питань


def read_token():
    # Функція повертає токен бота, отриманий у @BotFather.
    # На сервері токен зберігається у змінній середовища BOT_TOKEN.
    # Для локального запуску його можна записати у файл token.txt поруч з програмою.
    token = os.environ.get("BOT_TOKEN", "")
    token_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token.txt")
    if token == "" and os.path.exists(token_file):
        with open(token_file, "r", encoding="utf-8") as file:
            token = file.read().strip()
    return token


TOKEN = read_token()
if TOKEN == "":
    print("The bot token is not found.")
    print("Set the environment variable BOT_TOKEN or save the token to the file token.txt")
    sys.exit(1)

# Створюємо об'єкт бота, через який надсилаються всі повідомлення
bot = telebot.TeleBot(TOKEN)

# Словник зі станом тесту кожного користувача: номер чату -> дані тесту.
# Завдяки цьому бот може одночасно тестувати кількох користувачів.
sessions = {}


def build_test():
    # Функція готує тест: копіює питання, перемішує варіанти відповідей
    # кожного питання і самі питання у випадковому порядку
    test = []
    for item in QUESTIONS:
        options = item["options"].copy()    # копія, щоб не змінювати початковий список
        correct = options[0]                # правильна відповідь стоїть першою
        random.shuffle(options)             # перемішуємо варіанти відповідей
        test.append({"question": item["question"], "options": options, "correct": correct})
    random.shuffle(test)                    # перемішуємо питання
    return test


def question_text(state):
    # Функція повертає текст поточного питання разом з його номером
    number = state["index"] + 1
    total = len(state["questions"])
    item = state["questions"][state["index"]]
    return "Question " + str(number) + " of " + str(total) + "\n" + item["question"]


def send_question(chat_id):
    # Функція надсилає користувачу поточне питання з кнопками-відповідями
    state = sessions[chat_id]
    item = state["questions"][state["index"]]

    # Створюємо клавіатуру з кнопок під повідомленням: кожна кнопка в окремому рядку
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(item["options"])):
        # callback_data - рядок, який бот отримає після натискання кнопки:
        # у ньому зберігаємо номер питання і номер вибраного варіанта
        data = "answer:" + str(state["index"]) + ":" + str(i)
        button = types.InlineKeyboardButton(text=item["options"][i], callback_data=data)
        keyboard.add(button)

    bot.send_message(chat_id, question_text(state), reply_markup=keyboard)


def send_result(chat_id):
    # Функція надсилає звіт за результатами тесту: бали, дату і тривалість
    state = sessions[chat_id]
    finished = datetime.now()

    # Тривалість тесту - різниця між часом завершення і часом початку
    seconds = int((finished - state["started"]).total_seconds())
    duration = str(seconds // 60) + " min " + str(seconds % 60) + " s"

    total = len(state["questions"])
    text = "The test is finished!\n"
    text += "Score: " + str(state["score"]) + " out of " + str(total) + "\n"
    text += "Date: " + state["started"].strftime("%d.%m.%Y %H:%M") + "\n"
    text += "Duration: " + duration + "\n\n"
    text += "Report:\n"
    for i in range(len(state["answers"])):
        if state["answers"][i]:
            text += str(i + 1) + ". correct\n"
        else:
            text += str(i + 1) + ". incorrect\n"
    text += "\nSend /start to take the test again."

    bot.send_message(chat_id, text)
    del sessions[chat_id]    # тест завершено - видаляємо його стан


# Декоратор message_handler реєструє функцію як обробник команди /start
@bot.message_handler(commands=["start"])
def start(message):
    # Початок тесту: створюємо новий стан для цього користувача
    chat_id = message.chat.id
    sessions[chat_id] = {
        "questions": build_test(),    # питання у випадковому порядку
        "index": 0,                   # номер поточного питання
        "score": 0,                   # кількість набраних балів
        "answers": [],                # True/False для кожної відповіді
        "started": datetime.now(),    # час початку тесту
    }
    bot.send_message(chat_id, "Hello! This is a test of 10 questions about Python.\n"
                              "Choose one of the four answers to each question.")
    send_question(chat_id)


@bot.message_handler(commands=["help"])
def help_command(message):
    # Коротка довідка про бота
    text = "Send /start to begin the test of 10 questions about Python."
    bot.send_message(message.chat.id, text)


def is_answer(call):
    # Функція-фільтр: повертає True, якщо натиснуто кнопку з варіантом відповіді
    return call.data.startswith("answer:")


# Декоратор callback_query_handler реєструє обробник натискань на кнопки
@bot.callback_query_handler(func=is_answer)
def handle_answer(call):
    chat_id = call.message.chat.id

    # Розбираємо дані кнопки: "answer:номер питання:номер варіанта"
    parts = call.data.split(":")
    question_index = int(parts[1])
    option_index = int(parts[2])

    # Кнопка "застаріла", якщо тест не розпочато або це питання вже пройдено
    state = sessions.get(chat_id)
    if state is None or question_index != state["index"]:
        bot.answer_callback_query(call.id, "This question is no longer active.")
        return

    item = state["questions"][state["index"]]
    chosen = item["options"][option_index]

    # Перевіряємо відповідь і одразу готуємо повідомлення про результат
    if chosen == item["correct"]:
        state["score"] += 1
        state["answers"].append(True)
        verdict = "Correct!"
    else:
        state["answers"].append(False)
        verdict = "Incorrect. The correct answer: " + item["correct"]

    # Повідомляємо Telegram, що натискання оброблено
    bot.answer_callback_query(call.id)

    # Замінюємо текст повідомлення з питанням: додаємо відповідь користувача
    # і результат. Кнопки при цьому зникають, тому відповісти двічі не можна.
    text = question_text(state) + "\n\nYour answer: " + chosen + "\n" + verdict
    bot.edit_message_text(text, chat_id=chat_id, message_id=call.message.message_id)

    # Переходимо до наступного питання або показуємо підсумок
    state["index"] += 1
    if state["index"] < len(state["questions"]):
        send_question(chat_id)
    else:
        send_result(chat_id)


# Обробник усіх інших текстових повідомлень
@bot.message_handler(content_types=["text"])
def other_message(message):
    bot.send_message(message.chat.id, "Send /start to begin the test.")


# Запускаємо бота: він постійно запитує у Telegram нові повідомлення
if __name__ == "__main__":
    print("The bot is running. Press Ctrl+C to stop.")
    bot.infinity_polling()
