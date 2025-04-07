from character import Character
import random

class Hero(Character):
    def __init__(self):
        super().__init__()
        # Roll dice for combat strength and health points
        self.combat_strength = random.randint(1, 6)
        self.health_points = random.randint(1, 6) + random.randint(1, 6)
        self.dream_level = 0  # Default dream level
    
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