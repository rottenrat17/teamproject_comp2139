import random
import os

class Quest:
    def __init__(self, name, description, difficulty, reward, location, required_items=None):
        self.name = name
        self.description = description
        self.difficulty = difficulty  # 1-5 scale
        self.reward = reward  # Health or strength points
        self.location = location  # Dream level where this quest is available
        self.required_items = required_items or []
        self.completed = False
        
    def __str__(self):
        return f"{self.name} - {self.description} (Difficulty: {self.difficulty}, Reward: {self.reward})"

class QuestSystem:
    def __init__(self):
        # Initialize with some predefined quests
        self.available_quests = [
            Quest("Dragon Slayer", "Defeat the dream dragon lurking in the cave", 5, 10, 3, ["sword"]),
            Quest("Lost Artifact", "Find the ancient artifact hidden in the forest", 3, 5, 2),
            Quest("Shadow Hunter", "Track down and defeat the shadow creatures", 4, 7, 2, ["lantern"]),
            Quest("Dream Whisperer", "Speak with the dream spirit and learn its secrets", 1, 3, 1),
            Quest("Forgotten Memory", "Recover a lost memory in the dream realm", 2, 4, 0),
            Quest("Nightmare's End", "Confront and overcome your worst nightmare", 5, 12, 3, ["courage"]),
            Quest("Crystal Collector", "Gather dream crystals scattered across the realm", 2, 4, 1),
            Quest("Riddle Master", "Solve the ancient riddles of the dream sphinx", 3, 6, 2),
            Quest("Dream Healer", "Heal the wounded dream creatures", 2, 5, 1, ["potion"]),
            Quest("Mind's Eye", "Unlock the power of the mind's eye", 4, 8, 3, ["meditation"])
        ]
        self.completed_quests = []
        self.player_inventory = []
        
    def get_available_quests(self, dream_level, hero_strength):
        """
        Use list comprehension to filter available quests based on dream level and hero strength
        """
        # Filter quests that are available in the current dream level and not completed
        # Also filter based on hero's strength compared to quest difficulty
        return [quest for quest in self.available_quests 
                if quest.location <= dream_level  # Quest is available in current dream level
                and not quest.completed  # Quest is not completed
                and quest.difficulty <= hero_strength + 2]  # Hero is strong enough (with some leeway)
    
    def can_start_quest(self, quest, hero):
        """
        Use nested conditionals to determine if player can start a quest
        """
        # First check if the quest is available at all
        if quest in self.available_quests and not quest.completed:
            # Then check if player meets the dream level requirement
            if quest.location <= hero.dream_level:
                # Then check if player has required items
                if quest.required_items:
                    # Check each required item
                    for item in quest.required_items:
                        if item not in self.player_inventory:
                            print(f"You need a {item} to start this quest!")
                            return False
                    # If we reach here, player has all required items
                    return True
                else:
                    # No required items for this quest
                    return True
            else:
                print(f"This quest is only available at dream level {quest.location} or higher!")
                return False
        else:
            print("This quest is not available!")
            return False
    
    def add_item_to_inventory(self, item):
        """Add an item to player's inventory"""
        self.player_inventory.append(item)
        print(f"Added {item} to inventory!")
    
    def complete_quest(self, quest, hero):
        """Mark a quest as completed and give reward"""
        if quest in self.available_quests:
            quest.completed = True
            self.available_quests.remove(quest)
            self.completed_quests.append(quest)
            
            # Apply reward (increase health or strength)
            if random.choice([True, False]):
                hero.health_points += quest.reward
                print(f"You gained {quest.reward} health points from completing the quest!")
            else:
                hero.combat_strength += quest.reward // 2  # Dividing by 2 as strength gain should be smaller
                print(f"You gained {quest.reward // 2} combat strength from completing the quest!")
            
            return True
        return False
    
    def generate_random_quest(self, dream_level):
        """Generate a random quest for the given dream level"""
        quest_types = ["Hunt", "Find", "Rescue", "Defeat", "Explore", "Collect", "Solve"]
        quest_targets = ["creature", "artifact", "prisoner", "enemy", "location", "items", "puzzle"]
        quest_name = f"{random.choice(quest_types)} the {random.choice(quest_targets)}"
        
        difficulty = min(5, max(1, dream_level + random.randint(-1, 2)))  # Based on dream level with some randomness
        reward = difficulty * random.randint(1, 3)  # Higher difficulty gives better rewards
        
        # Decide if quest requires items
        required_items = []
        if random.random() > 0.5:  # 50% chance to have required items
            possible_items = ["sword", "lantern", "potion", "key", "map", "compass", "courage", "meditation"]
            required_items = [random.choice(possible_items)]
        
        description = f"A level {difficulty} quest for dream level {dream_level}"
        return Quest(quest_name, description, difficulty, reward, dream_level, required_items)
        
    def save_quest_progress(self):
        """Save quest progress to a file"""
        try:
            with open("quest_save.txt", "w") as file:
                # Save completed quests
                file.write(f"{len(self.completed_quests)}\n")
                for quest in self.completed_quests:
                    file.write(f"{quest.name}|{quest.description}|{quest.difficulty}|{quest.reward}|{quest.location}\n")
                
                # Save inventory
                file.write(f"{len(self.player_inventory)}\n")
                for item in self.player_inventory:
                    file.write(f"{item}\n")
            
            print("Quest progress saved successfully!")
        except Exception as e:
            print(f"Error saving quest progress: {e}")
    
    def load_quest_progress(self):
        """Load quest progress from a file"""
        try:
            if not os.path.exists("quest_save.txt"):
                print("No quest save file found.")
                return False
            
            with open("quest_save.txt", "r") as file:
                lines = file.readlines()
                line_index = 0
                
                # Load completed quests
                num_completed = int(lines[line_index].strip())
                line_index += 1
                
                # Clear existing completed quests
                self.completed_quests = []
                
                for i in range(num_completed):
                    if line_index < len(lines):
                        quest_data = lines[line_index].strip().split('|')
                        line_index += 1
                        
                        if len(quest_data) >= 5:
                            name, description, difficulty, reward, location = quest_data
                            quest = Quest(name, description, int(difficulty), int(reward), int(location))
                            quest.completed = True
                            self.completed_quests.append(quest)
                            
                            # Remove from available quests if it exists
                            for avail_quest in self.available_quests[:]:  # Create a copy to iterate
                                if avail_quest.name == name:
                                    self.available_quests.remove(avail_quest)
                
                # Load inventory
                if line_index < len(lines):
                    num_items = int(lines[line_index].strip())
                    line_index += 1
                    
                    # Clear existing inventory
                    self.player_inventory = []
                    
                    for i in range(num_items):
                        if line_index < len(lines):
                            item = lines[line_index].strip()
                            self.player_inventory.append(item)
                            line_index += 1
                
                print("Quest progress loaded successfully!")
                return True
        except Exception as e:
            print(f"Error loading quest progress: {e}")
            return False 