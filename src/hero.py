from character import Character
import random

class Hero(Character):
    def __init__(self):
        super().__init__()
        # Roll dice for combat strength and health points
        self.combat_strength = random.randint(1, 6)
        self.health_points = random.randint(1, 6) + random.randint(1, 6)
        # New attributes for loot system
        self.level = 1
        self.experience = 0
        self.inventory = []
    
    def __del__(self):
        print("The Hero object is being destroyed by the garbage collector")
        super().__del__()
    
    def hero_attacks(self):
        return random.randint(1, 6) + self.combat_strength
    
    def add_to_inventory(self, item):
        """Add an item to hero's inventory"""
        self.inventory.append(item)
        print(f"Added {item.name} to inventory!")
    
    def gain_experience(self, amount):
        """Gain experience and level up if enough experience is gained"""
        self.experience += amount
        # Level up if experience reaches 100 * current level
        if self.experience >= 100 * self.level:
            self.level += 1
            print(f"LEVEL UP! Hero is now level {self.level}")
            # Boost stats on level up
            self.combat_strength += 1
            self.health_points += 2
            return True
        return False
    
    def show_inventory(self):
        """Display the hero's inventory"""
        if not self.inventory:
            print("Inventory is empty")
            return
        
        print("\n--- Hero Inventory ---")
        for i, item in enumerate(self.inventory, 1):
            print(f"{i}. {item}")
        print("---------------------") 