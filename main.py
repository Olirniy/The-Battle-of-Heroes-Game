import random
from time import sleep
import sys


class Hero:
    def __init__(self, name, health=100, attack_power=20, critical_chance=0.15):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.critical_chance = critical_chance
        self.special_charge = 0

    def evade(self):
        return False

    def attack(self, other):
        if random.random() < self.critical_chance:
            damage = round(self.attack_power * 1.5)
            print(f"⚡ КРИТИЧЕСКИЙ УДАР! {self.name} наносит {damage} урона!")
        else:
            damage = self.attack_power
            print(f"{self.name} атакует с силой {damage}")

        # Проверка на уклонение
        if other.evade():
            print(f"🎯 {other.name} ЛОВКО УКЛОНИЛСЯ от атаки!")
            return 0  # Урон не наносится

        other.health -= damage
        self.special_charge += 10
        return damage

    def is_alive(self):
        return self.health > 0

    def special_attack(self, other):
        pass

    def reset(self):
        """Сброс характеристик героя к начальным значениям"""
        self.health = self.__class__().health
        self.attack_power = self.__class__().attack_power
        self.special_charge = 0


class Warrior(Hero):
    def __init__(self, name):
        super().__init__(name, health=110, attack_power=25, critical_chance=0.2)
        self.rage_charged = False

    def special_attack(self, other):
        if self.special_charge >= 30:
            self.rage_charged = True
            self.special_charge = 0
            print(f"\n🔥 {self.name} впадает в БЕРСЕРКЕРСКУЮ ЯРОСТЬ!")

            # Рассчитываем базовый урон
            if random.random() < self.critical_chance:
                base_damage = round(self.attack_power * 1.5)
                print(f"⚡ КРИТИЧЕСКИЙ УДАР! {self.name} наносит {base_damage} урона!")
            else:
                base_damage = self.attack_power
                print(f"{self.name} атакует с силой {base_damage}")

            other.health -= base_damage  # Наносим базовый урон

            # Добавляем бонус от ярости
            bonus_damage = round(base_damage * 0.35)
            other.health -= bonus_damage
            print(f"🔥 Ярость добавляет {bonus_damage} дополнительного урона!")

            self.rage_charged = False  # Сбрасываем состояние ярости
            return base_damage + bonus_damage
        else:
            return super().attack(other)

    def attack(self, other):
        # Проверяем, достаточно ли заряда для специальной атаки
        if self.special_charge >= 30:
            return self.special_attack(other)
        else:
            # Обычная атака
            damage = super().attack(other)
            return damage


class Mage(Hero):
    def __init__(self, name):
        super().__init__(name, health=90, attack_power=18)

    def attack(self, other):
        if random.random() < 0.3:
            damage = super().attack(other)
            other.health -= damage
            print(f"✨ МАГИЧЕСКИЙ ДУБЛЬ! {self.name} атакует еще раз!")
            return damage * 2
        return super().attack(other)


class Archer(Hero):
    def __init__(self, name):
        super().__init__(name, attack_power=22, critical_chance=0.25)

    def evade(self):
        """Лучник имеет 25% шанс уклониться от атаки"""
        if random.random() < 0.25:
            self.special_charge += 20
            return True
        return False


class Game:
    def __init__(self):
        self.player = None
        self.computer = None
        self.player_class_choice = None
        self.player_name = None

    def create_hero(self, choice, name):
        classes = {
            1: Warrior,
            2: Mage,
            3: Archer
        }
        return classes[choice](name)

    def show_menu(self):
        print("\n")
        print("=" * 40)
        print("🎮 ДОБРО ПОЖАЛОВАТЬ В БИТВУ ГЕРОЕВ! 🎮")
        print("=" * 40)
        print("Выбери своего героя:")
        print("1. Воин 💢 - Высокий урон, ярость берсерка")
        print("2. Маг 🔮 - Шанс двойной атаки, низкая защита")
        print("3. Лучник 🏹 - Уклонение и критические удары")
        print("=" * 40)

    def get_player_choice(self):
        while True:
            try:
                choice = int(input("Введите номер класса (1-3): "))
                if 1 <= choice <= 3:
                    return choice
            except:
                pass
            print("Ошибка! Введите число от 1 до 3")

    def setup_game(self):
        self.show_menu()
        self.player_class_choice = self.get_player_choice()
        self.player_name = input("Введите имя вашего героя: ")
        self.reset_game()

    def reset_game(self, new_hero=False):
        """Сброс игры для новой битвы"""
        if new_hero:
            self.setup_game()
        else:
            self.player = self.create_hero(self.player_class_choice, self.player_name)
            computer_class = random.choice([Warrior, Mage, Archer])
            self.computer = computer_class("Компьютер")
            self.print_hero_info()

    def start_battle(self):
        round_num = 1
        while self.player.is_alive() and self.computer.is_alive():
            print(f"\n🛡️ РАУНД {round_num} 🛡️")
            self.player_turn()
            if not self.computer.is_alive():
                break
            self.computer_turn()
            round_num += 1

        self.declare_winner()
        self.ask_for_restart()

    def ask_for_restart(self):
        """Новая система продолжения игры"""
        print(f"\nЖелаете продолжить битву как {self.player.name}?")
        print("1 - Продолжить с текущим героем")
        print("2 - Сменить героя")
        print("Любая другая клавиша - Выход")

        choice = input("Ваш выбор: ").strip()

        if choice == '1':
            self.reset_game()
            self.start_battle()
        elif choice == '2':
            self.reset_game(new_hero=True)
            self.start_battle()
        else:
            print("\nСпасибо за игру! До встречи!")
            sys.exit()

    def print_hero_info(self):
        print("\n⚔️ НАЧИНАЕТСЯ БИТВА ⚔️")
        print(f"{self.player.name} ({self.player.__class__.__name__})")
        print(f"VS")
        print(f"{self.computer.name} ({self.computer.__class__.__name__})")
        print("=" * 40)

    def player_turn(self):
        input("\nНажмите Enter для атаки...")
        damage = self.player.attack(self.computer)
        self.print_status(damage, self.player, self.computer)

    def computer_turn(self):
        sleep(1)
        print("\nХод компьютера:")
        damage = self.computer.attack(self.player)
        self.print_status(damage, self.computer, self.player)

    def print_status(self, damage, attacker, defender):
        print(f"❤️У {defender.name} здоровье: {max(defender.health, 0)}")
        print("-" * 40)

    def declare_winner(self):
        print("\n🔥🔥🔥 БИТВА ЗАВЕРШЕНА! 🔥🔥🔥")
        if self.player.is_alive():
            print(f"🏆 {self.player.name} ПОБЕДИЛ!")
        else:
            print(f"☠️ {self.computer.name} ПОБЕДИЛ!")


if __name__ == "__main__":
    game = Game()
    game.setup_game()
    game.start_battle()