from character import Character
import random

class Monster(Character):
    """
    Represents a monster in the game. Inherits from Character.
    Handles monster-specific attack logic.
    """
    def __init__(self):
        super().__init__()
    
    def monster_attacks(self, hero):
        """
        Simulates the monster attacking the hero.
        Reduces the hero's health points based on the monster's combat strength.
        """
        print(f"Monster attacks! Monster Strength: {self.combat_strength}, Hero HP: {hero.health_points}")
        if self.combat_strength >= hero.health_points:
            hero.health_points = 0
            print("The monster has defeated the hero!")
        else:
            hero.health_points -= self.combat_strength
            print(f"The hero now has {hero.health_points} HP left.")
    
    def __del__(self):
        try:
            print("The Monster object is being destroyed by the garbage collector")
        except Exception as e:
            print(f"Error during destruction: {e}")
