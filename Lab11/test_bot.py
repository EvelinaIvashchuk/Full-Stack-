# Лабораторна робота №11. Telegram-бот
# Виконала: Іващук Евеліна

# Тести логіки бота (фреймворк unittest). Тести не підключаються до Telegram:
# методи бота, які надсилають повідомлення, замінено об'єктами MagicMock,
# що лише запам'ятовують, з якими аргументами їх викликали.

import os
import unittest
from types import SimpleNamespace    # простий об'єкт з довільними атрибутами
from unittest.mock import MagicMock

# Бот читає токен під час імпорту, тому для тестів задаємо несправжній токен
os.environ["BOT_TOKEN"] = "123456:TEST-TOKEN"

import bot as quiz_bot
from questions import QUESTIONS

CHAT_ID = 111


def make_message():
    # Несправжнє повідомлення користувача з номером чату
    return SimpleNamespace(chat=SimpleNamespace(id=CHAT_ID))


def make_call(data):
    # Несправжнє натискання кнопки з даними data
    message = SimpleNamespace(chat=SimpleNamespace(id=CHAT_ID), message_id=1)
    return SimpleNamespace(id="1", data=data, message=message)


class TestBot(unittest.TestCase):

    def setUp(self):
        # Перед кожним тестом очищаємо стан і замінюємо мережеві методи бота
        quiz_bot.sessions.clear()
        quiz_bot.bot.send_message = MagicMock()
        quiz_bot.bot.edit_message_text = MagicMock()
        quiz_bot.bot.answer_callback_query = MagicMock()

    def answer(self, correct):
        # Допоміжний метод: відповідає на поточне питання правильно або неправильно
        state = quiz_bot.sessions[CHAT_ID]
        item = state["questions"][state["index"]]
        correct_index = item["options"].index(item["correct"])
        if correct:
            option = correct_index
        else:
            option = (correct_index + 1) % 4
        data = "answer:" + str(state["index"]) + ":" + str(option)
        quiz_bot.handle_answer(make_call(data))

    def test_there_are_ten_questions_with_four_options(self):
        self.assertEqual(len(QUESTIONS), 10)
        for item in QUESTIONS:
            self.assertEqual(len(item["options"]), 4)
            self.assertEqual(len(set(item["options"])), 4)    # варіанти не повторюються

    def test_build_test_keeps_questions_and_answers(self):
        # Після перемішування мають залишитися ті самі питання і відповіді
        test = quiz_bot.build_test()
        self.assertEqual(len(test), 10)
        for item in test:
            original = [q for q in QUESTIONS if q["question"] == item["question"]][0]
            self.assertEqual(sorted(item["options"]), sorted(original["options"]))
            self.assertEqual(item["correct"], original["options"][0])

    def test_order_is_random(self):
        # Серед 20 підготовлених тестів порядок питань має відрізнятися
        orders = set()
        for i in range(20):
            orders.add(tuple(item["question"] for item in quiz_bot.build_test()))
        self.assertGreater(len(orders), 1)

    def test_start_sends_first_question_with_four_buttons(self):
        quiz_bot.start(make_message())
        self.assertEqual(quiz_bot.sessions[CHAT_ID]["index"], 0)
        # Останнє надіслане повідомлення - перше питання з клавіатурою
        args, kwargs = quiz_bot.bot.send_message.call_args
        self.assertIn("Question 1 of 10", args[1])
        self.assertEqual(len(kwargs["reply_markup"].keyboard), 4)

    def test_correct_answer_adds_point(self):
        quiz_bot.start(make_message())
        self.answer(correct=True)
        state = quiz_bot.sessions[CHAT_ID]
        self.assertEqual(state["score"], 1)
        self.assertEqual(state["index"], 1)
        text = quiz_bot.bot.edit_message_text.call_args[0][0]
        self.assertIn("Correct!", text)

    def test_wrong_answer_shows_correct_one(self):
        quiz_bot.start(make_message())
        correct = quiz_bot.sessions[CHAT_ID]["questions"][0]["correct"]
        self.answer(correct=False)
        self.assertEqual(quiz_bot.sessions[CHAT_ID]["score"], 0)
        text = quiz_bot.bot.edit_message_text.call_args[0][0]
        self.assertIn("Incorrect. The correct answer: " + correct, text)

    def test_old_button_is_ignored(self):
        # Повторне натискання кнопки вже пройденого питання не змінює результат
        quiz_bot.start(make_message())
        self.answer(correct=True)
        quiz_bot.handle_answer(make_call("answer:0:0"))
        state = quiz_bot.sessions[CHAT_ID]
        self.assertEqual(state["index"], 1)
        self.assertEqual(len(state["answers"]), 1)

    def test_button_without_test_is_ignored(self):
        # Натискання кнопки, коли тест не розпочато, не викликає помилки
        quiz_bot.handle_answer(make_call("answer:0:0"))
        quiz_bot.bot.edit_message_text.assert_not_called()

    def test_full_test_result(self):
        # Проходимо весь тест: 7 правильних відповідей і 3 неправильні
        quiz_bot.start(make_message())
        for i in range(10):
            self.answer(correct=(i < 7))
        result = quiz_bot.bot.send_message.call_args[0][1]
        self.assertIn("Score: 7 out of 10", result)
        self.assertIn("Date:", result)
        self.assertIn("Duration:", result)
        self.assertIn("8. incorrect", result)
        # Після завершення тесту його стан видаляється
        self.assertNotIn(CHAT_ID, quiz_bot.sessions)


if __name__ == "__main__":
    unittest.main(verbosity=2)
