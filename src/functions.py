import random

def use_loot(belt, health_points):
    """
    Uses the first item in the belt. Adjusts health points based on the item.
    """
    good_loot_options = ["Health Potion", "Leather Boots"]
    bad_loot_options = ["Poison Potion"]
    first_item = belt.pop(0)
    if first_item in good_loot_options:
        health_points = min(20, health_points + 2)
    elif first_item in bad_loot_options:
        health_points = max(0, health_points - 2)
    return belt, health_points

def collect_loot(loot_options, belt):
    """
    Collects a random loot item and adds it to the belt.
    """
    loot_roll = random.choice(range(len(loot_options)))
    loot = loot_options.pop(loot_roll)
    belt.append(loot)
    return loot_options, belt

def adjust_combat_strength(combat_strength, m_combat_strength):
    """
    Adjusts combat strength based on the result of the last game.
    """
    last_game = load_game()
    if last_game and "Hero" in last_game:
        m_combat_strength += 1
    elif last_game and "Monster" in last_game:
        combat_strength += 1

def save_game(winner, hero_name="", num_stars=0):
    """
    Saves the game result to a file.
    """
    try:
        with open("save.txt", "a") as file:
            file.write(f"{winner} won. {hero_name} earned {num_stars} stars.\n")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game():
    """
    Loads the last game result from a file.
    """
    try:
        with open("save.txt", "r") as file:
            lines = file.readlines()
            return lines[-1] if lines else None
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error loading game: {e}")
        return None

# Quest System Functions
def generate_quests(player_level, completed_quests=None):
    """
    Generates a list of available quests using list comprehension
    Filters based on previously completed quests
    """
    if completed_quests is None:
        completed_quests = []
    
    # All possible quests as shown in the diagram
    all_quests = [
        {"id": 1, "name": "Defeat Goblin", "type": "combat"},
        {"id": 2, "name": "Collect Herbs", "type": "gathering"},
        {"id": 3, "name": "Rescue Villager", "type": "rescue"},
        {"id": 4, "name": "Find Treasure", "type": "exploration"}
    ]
    
    # List comprehension to filter out completed quests
    available_quests = [quest for quest in all_quests 
                        if quest["id"] not in completed_quests]
    
    return available_quests

def can_start_quest(quest, hero):
    """
    Uses nested conditional statements to determine if a player can start a quest
    Following the exact logic from the diagram
    """
    # Forest Guardian quest logic (assuming this is part of "Defeat Goblin" quest)
    if quest["name"] == "Defeat Goblin":
        # Check if player is in correct location (Forest)
        if hero.current_location == "forest":
            # Check if player has magic sword
            if "magic sword" in hero.inventory:
                # Can fight Forest Guardian with sword
                return True, "Can fight Forest Guardian!"
            else:
                # Check if strength > 7
                if hero.combat_strength > 7:
                    # Can fight with brute strength
                    return True, "Can fight with brute strength!"
                else:
                    # Need more power or sword
                    return False, "Need more power or sword"
        else:
            # Wrong location
            return False, "Wrong location"
    
    # Collect Herbs quest
    elif quest["name"] == "Collect Herbs":
        # This quest is shown as completed/filtered out in the diagram
        return False, "Quest already completed"
    
    # Rescue Villager quest
    elif quest["name"] == "Rescue Villager":
        # Basic check - available if in village or forest
        if hero.current_location in ["village", "forest"]:
            return True, "Ready to rescue villagers"
        else:
            return False, "Need to be in village or forest"
    
    # Find Treasure quest
    elif quest["name"] == "Find Treasure":
        # Basic check - need a map
        if "map" in hero.inventory:
            return True, "Ready to find treasure"
        else:
            return False, "Need a map for treasure hunting"
    
    # Default case
    return False, "Quest unavailable"

def complete_quest(quest_id, completed_quests=None):
    """
    Marks a quest as completed and adds it to the completed quests list
    """
    if completed_quests is None:
        completed_quests = []
    
    if quest_id not in completed_quests:
        completed_quests.append(quest_id)
    
    return completed_quests

def save_quest_progress(player_name, completed_quests):
    """
    Saves the player's quest progress to a file
    """
    try:
        with open(f"{player_name}_quests.txt", "w") as file:
            for quest_id in completed_quests:
                file.write(f"{quest_id}\n")
    except Exception as e:
        print(f"Error saving quest progress: {e}")

def load_quest_progress(player_name):
    """
    Loads the player's quest progress from a file
    """
    completed_quests = []
    try:
        with open(f"{player_name}_quests.txt", "r") as file:
            for line in file:
                completed_quests.append(int(line.strip()))
    except FileNotFoundError:
        # No previous quest progress found, return empty list
        pass
    except Exception as e:
        print(f"Error loading quest progress: {e}")
    
    return completed_quests
