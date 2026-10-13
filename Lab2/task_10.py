# Лабораторна робота №2. Рядки. Завдання 10
# Виконала: Іващук Евеліна

# Завдання 10. Дано рядок на англійській мові, що містить текст (до тисячі
# слів). Вивести всі слова, що починаються на літеру N і слова, що
# закінчуються на літеру P. Літери N і P вводяться користувачем.

# Вводимо текст і дві літери з клавіатури
text = input("Enter the text: ")
n = input("Enter the letter N (the beginning of a word): ")
p = input("Enter the letter P (the end of a word): ")

# Переводимо літери в нижній регістр, щоб пошук не залежав від регістру
n = n.lower()
p = p.lower()

starts_with_n = []    # слова, що починаються на літеру N
ends_with_p = []      # слова, що закінчуються на літеру P

for word in text.split():
    # Прибираємо розділові знаки з початку і кінця слова
    word = word.strip('.,!?;:()"')

    # startswith() перевіряє початок рядка, endswith() - його кінець
    if word.lower().startswith(n):
        starts_with_n.append(word)
    if word.lower().endswith(p):
        ends_with_p.append(word)

print("Words starting with", n, ":", starts_with_n)
print("Words ending with", p, ":", ends_with_p)
