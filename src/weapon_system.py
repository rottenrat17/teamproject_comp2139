# Weapon System by Jeevan

import random

class WeaponSystem:
    def __init__(self):
        self.weapon_types = ["Rusty Dagger", "Battle Axe", "Magic Wand", "Enchanted Sword", "Dragon Slayer"]
        self.drop_chance = 0.65  # 65% chance for a weapon to drop
        
    def apply_weapon_effect(self, monster):
        """
        Attempts to apply a weapon effect on the monster, reducing its strength
        Returns True if effect applied, False otherwise
        """
        if random.random() < self.drop_chance:
            # Calculate strength reduction (2-3 points)
            strength_reduction = random.randint(2, 3)
            
            # Select a random weapon
            weapon = random.choice(self.weapon_types)
            
            # Ensure monster strength doesn't go below 1
            if monster.m_combat_strength > strength_reduction:
                monster.m_combat_strength -= strength_reduction
                print(f"\n*** WEAPON DROP: {weapon} ***")
                print(f"The {weapon} weakens the monster by {strength_reduction} strength points!")
                return True
            else:
                # If monster would go below 1 strength, set to 1
                strength_reduction = monster.m_combat_strength - 1
                if strength_reduction > 0:
                    monster.m_combat_strength = 1
                    print(f"\n*** WEAPON DROP: {weapon} ***")
                    print(f"The {weapon} weakens the monster to minimum strength!")
                    return True
        
        return False
