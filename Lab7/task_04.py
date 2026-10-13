# Лабораторна робота №7. Класи. Частина 2. Завдання 4
# Виконала: Іващук Евеліна

# Завдання 4. Напишіть клас Dog, який має три атрибути класу: mammal
# (ссавець), nature (характер) і breed (порода), та два атрибути екземпляра:
# name (кличка) і age (вік). Створіть екземпляри трьох нових собак, кожна з
# яких різного віку. Визначте у класі Dog метод для виведення значень
# атрибутів екземпляру - імені та віку конкретної собаки. За потреби додайте
# кілька інших методів, які визначають поведінку собаки. Напишіть кілька
# класів, які унаслідуються від батьківського класу Dog, що описують
# конкретні породи собак. Визначте для цих класів атрибути nature і breed
# відповідно, включіть у класи по одному методу, що визначає поведінку
# конкретної породи собаки. Створіть батьківський клас Pets, що створює
# список ваших домашніх улюбленців. У підсумку надрукуйте інформацію про
# ваших домашніх тварин.


class Dog:
    # Атрибути класу спільні для всіх екземплярів цього класу
    mammal = True          # собака - ссавець
    nature = "unknown"     # характер
    breed = "unknown"      # порода

    def __init__(self, name, age):
        # Атрибути екземпляра у кожної собаки свої
        self.name = name    # кличка
        self.age = age      # вік

    def description(self):
        # Метод виводить кличку і вік конкретної собаки
        print(self.name, "is", self.age)

    def speak(self):
        # Метод описує поведінку собаки - подавання голосу
        print(self.name, "says: Woof!")


# Запис class Labrador(Dog) означає, що клас Labrador успадковує від класу Dog
# усі його атрибути і методи. У класі-нащадку перевизначаємо атрибути
# nature і breed та додаємо метод, властивий лише цій породі.
class Labrador(Dog):
    nature = "friendly"
    breed = "Labrador"

    def fetch(self):
        print(self.name, "fetches the ball")


class Bulldog(Dog):
    nature = "calm"
    breed = "Bulldog"

    def guard(self):
        print(self.name, "guards the house")


class Husky(Dog):
    nature = "energetic"
    breed = "Husky"

    def run(self):
        print(self.name, "runs very fast")


class Pets:
    # Клас зберігає список домашніх улюбленців

    def __init__(self, dogs):
        self.dogs = dogs    # список об'єктів-собак

    def show(self):
        # Метод виводить інформацію про всіх домашніх тварин
        print("I have", len(self.dogs), "dogs.")
        for dog in self.dogs:
            dog.description()
            print("  breed:", dog.breed, ", nature:", dog.nature)

        # Перевіряємо, чи всі тварини є ссавцями
        all_mammals = True
        for dog in self.dogs:
            if not dog.mammal:
                all_mammals = False
        if all_mammals:
            print("And they are all mammals, of course.")


# Створюємо трьох собак різного віку
tom = Labrador("Tom", 6)
fletcher = Bulldog("Fletcher", 7)
larry = Husky("Larry", 9)

# Створюємо список домашніх улюбленців і виводимо інформацію про них
my_pets = Pets([tom, fletcher, larry])
my_pets.show()

# Викликаємо метод, успадкований від класу Dog, і методи окремих порід
print()
tom.speak()
tom.fetch()
fletcher.guard()
larry.run()
