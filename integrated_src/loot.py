import random

class Item:
    def __init__(self, name, type, effect_value):
        self.name = name
        self.type = type  # "weapon", "armor", "potion", "amulet"
        self.effect_value = effect_value
    
    def __str__(self):
        return f"{self.name} ({self.type}): +{self.effect_value} {self._get_effect_type()}"
    
    def _get_effect_type(self):
        if self.type == "weapon":
            return "attack"
        elif self.type == "armor":
            return "defense"
        elif self.type == "potion":
            return "health"
        elif self.type == "amulet":
            return "magic power"
        return ""

class LootSystem:
    def __init__(self):
        self.available_items = [
            Item("Wooden Sword", "weapon", 1),
            Item("Steel Dagger", "weapon", 2),
            Item("Magic Staff", "weapon", 4),
            Item("Leather Armor", "armor", 1),
            Item("Dragon Scale", "armor", 3),
            Item("Health Potion", "potion", 5),
            Item("Golden Amulet", "amulet", 2)
        ]
    
    def get_loot(self, monster, hero_level):
        """Use list comprehension to filter potential drops based on monster and hero level"""
        # Filter items based on hero level - higher level heroes can get better items
        potential_drops = [item for item in self.available_items 
                          if (hero_level >= 2 and item.effect_value >= 3) or 
                             (hero_level < 2 and item.effect_value <= 3)]
        
        # Determine if a monster drops an item (50% chance)
        if random.random() < 0.5:
            return random.choice(potential_drops)
        return None
    
    def apply_item_effect(self, hero, item):
        """Apply item effects using nested conditional statements"""
        if item.type == "weapon":
            # Weapon increases combat strength
            hero.combat_strength += item.effect_value
            print(f"Hero's combat strength increased to {hero.combat_strength}")
        elif item.type == "armor":
            # Armor adds to health points
            hero.health_points += item.effect_value
            print(f"Hero's health increased to {hero.health_points}")
        elif item.type == "potion":
            # Potions provide immediate health restoration
            if hero.health_points < 10:
                # Larger health boost for heroes with low health
                hero.health_points += item.effect_value
                print(f"Hero consumed potion and recovered {item.effect_value} health. New health: {hero.health_points}")
            else:
                # Smaller boost for heroes with high health
                boost = item.effect_value // 2
                hero.health_points += boost
                print(f"Hero already healthy, potion restored only {boost} health. New health: {hero.health_points}")
        elif item.type == "amulet":
            # Amulet increases both combat strength and health
            hero.combat_strength += item.effect_value
            hero.health_points += item.effect_value
            print(f"Golden Amulet's magic flows through you! Combat strength: {hero.combat_strength}, Health: {hero.health_points}")
        
        return hero 