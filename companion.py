class Companion:
    def __init__(self, name, role):
        self.name = name
        self.role = role.lower()
        self.power = self.set_power()

    def set_power(self):
        if self.role == 'healer':
            return 5
        elif self.role == 'fighter':
            return 7
        elif self.role == 'guardian':
            return 3
        else:
            return 0

    def assist(self, hero):
        if self.role == 'healer':
            hero.health_points += self.power
            print(f"{self.name} heals {hero.name} for {self.power} HP!")
        elif self.role == 'fighter':
            hero.combat_strength += self.power
            print(f"{self.name} boosts {hero.name}'s attack by {self.power}!")
        elif self.role == 'guardian':
            hero.health_points += 2
            hero.combat_strength += 1
            print(f"{self.name} provides defense and a small attack bonus!")
        else:
            print(f"{self.name} is unsure how to help...")

    def __repr__(self):
        return f"Companion({self.name}, {self.role}, power={self.power})" 