from character import Character
import random

class Hero(Character):
    def __init__(self, name="Adventurer"):
        super().__init__()
        self.name = name
        # Roll dice for combat strength and health points
        self.combat_strength = random.randint(1, 6)
        self.health_points = random.randint(1, 6) + random.randint(1, 6)
        self.dream_level = 0  # Default dream level
        self.companion = None  # Initialize companion as None
    
    def __del__(self):
        print("The Hero object is being destroyed by the garbage collector")
        super().__del__()
    
    def hero_attacks(self):
        return random.randint(1, 6) + self.combat_strength
        
    def set_dream_level(self, level):
        """Set the hero's current dream level"""
        if 0 <= level <= 3:
            self.dream_level = level
            return True
        return False
        
    def set_companion(self, companion):
        """Set the hero's companion"""
        self.companion = companion
        print(f"{self.name} is now accompanied by {companion.name} the {companion.role}!")
        
    def use_companion_ability(self):
        """Use the companion's ability to assist the hero"""
        if self.companion:
            self.companion.assist(self)
            return True
        else:
            print(f"{self.name} has no companion to help!")
            return False 