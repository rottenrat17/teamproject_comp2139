from character import Character
import random

class Hero(Character):
    def __init__(self):
        super().__init__()
        # Roll dice for combat strength and health points
        self.combat_strength = random.randint(1, 6)
        self.health_points = random.randint(1, 6) + random.randint(1, 6)
    
    def __del__(self):
        print("The Hero object is being destroyed by the garbage collector")
        super().__del__()
    
    def hero_attacks(self, weather=None):
        attack_power = random.randint(1, 6) + self.combat_strength
        
        # Apply weather effects if provided
        if weather:
            from functions import get_weather_effects
            weather_effect = get_weather_effects(weather)
            attack_power += weather_effect["hero_effect"]
            
            # Ensure attack power is at least 1
            attack_power = max(1, attack_power)
            
        return attack_power 