class Character:
    def __init__(self):
        self.__combat_strength = 0
        self.__health_points = 0
    
    def __del__(self):
        print("The Character object is being destroyed by the garbage collector")
    
    @property
    def combat_strength(self):
        return self.__combat_strength
    
    @combat_strength.setter
    def combat_strength(self, value):
        self.__combat_strength = value
    
    @property
    def health_points(self):
        return self.__health_points
    
    @health_points.setter
    def health_points(self, value):
        self.__health_points = value 