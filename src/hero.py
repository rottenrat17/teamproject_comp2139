import random
import os
import platform
from monster import Monster
try:
    from . import functions
except ImportError:
    try:
        import functions
    except ImportError:
        print("Error: 'functions' module not found. Ensure 'functions.py' is in the same directory or properly installed.")
        exit(1)
import time  # Add this import for introducing delays
import gc  # Import garbage collector module

class Hero:
    def __init__(self):
        self.health_points = 10
        self.combat_strength = 5
        self.level = 1
        self.xp = 0
        self.inventory = []
        self.current_location = "town"
        self.completed_quests = []
        self.active_quest = None

    def hero_attacks(self, monster):
        damage = self.combat_strength
        monster.health_points = max(0, monster.health_points - damage)  # Ensure health_points does not go below zero
        print(f"Hero attacks Monster for {damage} damage. Monster HP: {monster.health_points}")
    
    def gain_xp(self, amount):
        """
        Grants XP to the hero and levels up if enough XP is gained
        """
        self.xp += amount
        if self.xp >= self.level * 10:  # Simple level-up formula
            self.level_up()
    
    def level_up(self):
        """
        Increases hero's level and stats
        """
        self.level += 1
        self.combat_strength += 1
        self.health_points = min(20, self.health_points + 5)  # Cap at 20 HP
        print(f"Level up! You are now level {self.level}!")
        print(f"Combat Strength: {self.combat_strength}, Health: {self.health_points}")
    
    def add_to_inventory(self, item):
        """
        Adds an item to the hero's inventory
        """
        self.inventory.append(item)
        print(f"Added {item} to inventory")
    
    def view_available_quests(self):
        """
        Shows available quests to the player using list comprehension
        """
        available_quests = functions.generate_quests(self.level, self.completed_quests)
        if not available_quests:
            print("No quests available!")
            return None
        
        print("\nAvailable Quests:")
        for i, quest in enumerate(available_quests):
            print(f"{i+1}. {quest['name']} ({quest['type']} quest)")
        
        return available_quests
    
    def start_quest(self, quest_index, available_quests):
        """
        Attempts to start a quest using nested conditional logic as shown in the diagram
        """
        if 0 <= quest_index < len(available_quests):
            selected_quest = available_quests[quest_index]
            can_start, message = functions.can_start_quest(selected_quest, self)
            
            if can_start:
                self.active_quest = selected_quest
                print(f"Quest started: {selected_quest['name']}")
                print(f"Quest status: {message}")
                return True
            else:
                print(f"Cannot start quest: {message}")
        return False
    
    def complete_active_quest(self):
        """
        Completes the active quest, grants rewards
        """
        if self.active_quest:
            print(f"Quest completed: {self.active_quest['name']}")
            # Grant XP based on quest type
            xp_reward = 5  # Default XP
            if self.active_quest['type'] == 'combat':
                xp_reward = 10
            elif self.active_quest['type'] == 'exploration':
                xp_reward = 7
            elif self.active_quest['type'] == 'rescue':
                xp_reward = 8
            elif self.active_quest['type'] == 'gathering':
                xp_reward = 6
            
            self.gain_xp(xp_reward)
            print(f"You gained {xp_reward} XP!")
            
            self.completed_quests = functions.complete_quest(self.active_quest['id'], self.completed_quests)
            functions.save_quest_progress("Player1", self.completed_quests)
            self.active_quest = None
            return True
        return False
    
    def change_location(self, new_location):
        """
        Changes the hero's current location
        """
        valid_locations = ["town", "forest", "cave", "mountain", "village"]
        if new_location in valid_locations:
            self.current_location = new_location
            print(f"You have traveled to the {new_location}")
            return True
        print("Invalid location!")
        return False
