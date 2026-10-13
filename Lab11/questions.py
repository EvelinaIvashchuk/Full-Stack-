# Лабораторна робота №11. Telegram-бот
# Виконала: Іващук Евеліна

# Модуль questions містить тестові питання про мову Python.
# Кожне питання - словник з текстом питання і списком із чотирьох варіантів
# відповіді. Правильна відповідь завжди стоїть у списку першою; перед показом
# користувачу бот перемішує варіанти у випадковому порядку.

QUESTIONS = [
    {
        "question": "Which keyword is used to define a function in Python?",
        "options": ["def", "function", "func", "define"],
    },
    {
        "question": "What is the result of the expression 7 // 2?",
        "options": ["3", "3.5", "4", "1"],
    },
    {
        "question": "Which of these data types is immutable?",
        "options": ["tuple", "list", "dict", "set"],
    },
    {
        "question": "What does the expression [x * 2 for x in range(3)] create?",
        "options": ["[0, 2, 4]", "[2, 4, 6]", "[0, 1, 2]", "[1, 2, 3]"],
    },
    {
        "question": "Which construction is used to handle exceptions?",
        "options": ["try ... except", "try ... catch", "do ... rescue", "if ... error"],
    },
    {
        "question": "Which method is called automatically when an object is created?",
        "options": ["__init__", "__start__", "__create__", "__object__"],
    },
    {
        "question": "What is the first parameter of an instance method usually called?",
        "options": ["self", "this", "me", "object"],
    },
    {
        "question": "How do you declare that the class Dog inherits from the class Animal?",
        "options": ["class Dog(Animal):", "class Dog extends Animal:",
                    "class Dog inherits Animal:", "class Dog <- Animal:"],
    },
    {
        "question": "Which function gives access to the methods of the parent class?",
        "options": ["super()", "parent()", "base()", "upper()"],
    },
    {
        "question": "Which library is used for working with tables of data (DataFrame)?",
        "options": ["pandas", "requests", "unittest", "random"],
    },
]
