# Лабораторна робота №8. Класи. Частина 3. Завдання 3
# Виконала: Іващук Евеліна

# Завдання 3. Створіть клас Apple зі статичним атрибутом states (стадії
# дозрівання яблука), захищеними атрибутами _index і _state та методами
# grow() і is_ripe(). Створіть клас AppleTree зі списком яблук apples і
# методами grow_all(), all_are_ripe(), give_away_all(). Створіть клас Gardener
# з атрибутами name і _tree, методами work() і harvest() та статичним
# методом apple_base().


class Apple:
    # Статичний атрибут: словник з усіма стадіями дозрівання яблука
    states = {0: "Absent", 1: "Flowering", 2: "Green", 3: "Red"}

    def __init__(self, index):
        self._index = index    # номер яблука
        self._state = 0        # перша стадія зі словника states

    def grow(self):
        # Метод переводить яблуко на наступну стадію дозрівання,
        # якщо воно ще не досягло останньої
        if self._state < len(Apple.states) - 1:
            self._state += 1

    def is_ripe(self):
        # Метод перевіряє, чи яблуко дозріло (досягло останньої стадії)
        return self._state == len(Apple.states) - 1


class AppleTree:
    def __init__(self, count):
        # Створюємо список з count об'єктів класу Apple
        self.apples = []
        for index in range(count):
            self.apples.append(Apple(index))

    def grow_all(self):
        # Метод переводить усі яблука на наступний етап дозрівання
        for apple in self.apples:
            apple.grow()

    def all_are_ripe(self):
        # Метод повертає True, якщо всі яблука стали стиглими
        for apple in self.apples:
            if not apple.is_ripe():
                return False
        return True

    def give_away_all(self):
        # Метод очищає список яблук після збору врожаю
        self.apples = []


class Gardener:
    def __init__(self, name, tree):
        self.name = name     # ім'я садівника, публічний атрибут
        self._tree = tree    # дерево, за яким доглядає садівник

    def work(self):
        # Садівник працює - яблука стають більш стиглими
        print(self.name, "is working...")
        self._tree.grow_all()

    def harvest(self):
        # Садівник збирає врожай, якщо всі плоди дозріли
        if self._tree.all_are_ripe():
            print(self.name, "harvested", len(self._tree.apples), "apples")
            self._tree.give_away_all()
        else:
            print("Warning: the apples are not ripe yet!")

    @staticmethod
    def apple_base(apples):
        # Статичний метод виводить довідку: кількість яблук і ступінь їх стиглості
        print("Number of apples:", len(apples))
        for apple in apples:
            print("Apple", apple._index, "-", Apple.states[apple._state])


# ---------- Тести до модуля ----------

# Створюємо декілька об'єктів класу Apple
apple1 = Apple(1)
apple2 = Apple(2)
apple2.grow()

# Викликаємо довідку по всіх наявних яблуках
Gardener.apple_base([apple1, apple2])
print()

# Створюємо об'єкти класів AppleTree і Gardener
tree = AppleTree(3)
gardener = Gardener("Ivan", tree)

# Садівник працює над яблучним деревом
gardener.work()
Gardener.apple_base(tree.apples)

# Пробуємо зібрати врожай: яблука ще не дозріли
gardener.harvest()

# Продовжуємо доглядати за деревом, поки всі яблука не дозріють
while not tree.all_are_ripe():
    gardener.work()
Gardener.apple_base(tree.apples)

# Збираємо врожай
gardener.harvest()
Gardener.apple_base(tree.apples)
