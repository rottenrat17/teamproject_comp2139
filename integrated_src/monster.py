from character import Character
import random

class Monster(Character):
    def __init__(self):
        super().__init__()
        # Roll dice for combat strength and health points
        self.__m_combat_strength = random.randint(1, 6)
        self.__m_health_points = random.randint(1, 6) + random.randint(1, 6)
    
    def __del__(self):
        print("The Monster object is being destroyed by the garbage collector")
        super().__del__()
    
    def monster_attacks(self, weather=None):
        attack_power = random.randint(1, 6) + self.m_combat_strength
        
        # Apply weather effects if provided
        if weather:
            from functions import get_weather_effects
            weather_effect = get_weather_effects(weather)
            attack_power += weather_effect["monster_effect"]
            
            # Ensure attack power is at least 1
            attack_power = max(1, attack_power)
            
        return attack_power
    
    @property
    def m_combat_strength(self):
        return self.__m_combat_strength
    
    @m_combat_strength.setter
    def m_combat_strength(self, value):
        self.__m_combat_strength = value
    
    @property
    def m_health_points(self):
        return self.__m_health_points
    
    @m_health_points.setter
    def m_health_points(self, value):
        self.__m_health_points = value
        
    # Properties to maintain compatibility with Character class
    @property
    def combat_strength(self):
        return self.m_combat_strength
    
    @combat_strength.setter
    def combat_strength(self, value):
        self.m_combat_strength = value
    
    @property
    def health_points(self):
        return self.m_health_points
    
    @health_points.setter
    def health_points(self, value):
        self.m_health_points = value 