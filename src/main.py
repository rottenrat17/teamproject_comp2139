import random
import os
import platform
from hero import Hero
from monster import Monster
import functions
import time  # Add this import for introducing delays

# Define functions first before using them
def display_quest_diagram(hero):
    """
    Displays a visual representation of quests similar to the diagram
    """
    all_quests = [
        {"id": 1, "name": "Defeat Goblin", "type": "combat"},
        {"id": 2, "name": "Collect Herbs", "type": "gathering"},
        {"id": 3, "name": "Rescue Villager", "type": "rescue"},
        {"id": 4, "name": "Find Treasure", "type": "exploration"}
    ]
    
    available_quests = [quest for quest in all_quests if quest["id"] not in hero.completed_quests]
    
    print("\n+" + "-" * 26 + "+")
    print("|" + "All Quests".center(26) + "|")
    print("+" + "-" * 26 + "+")
    
    for quest in all_quests:
        status = " (X)" if quest["id"] in hero.completed_quests else ""
        print("| " + f"{quest['id']}. {quest['name']}{status}".ljust(24) + " |")
    
    print("+" + "-" * 26 + "+")
    print("|" + "↓".center(26) + "|")
    print("[List Comprehension]".center(28))
    
    print("+" + "-" * 26 + "+")
    print("|" + "Available Quests".center(26) + "|")
    print("+" + "-" * 26 + "+")
    
    for i, quest in enumerate(available_quests, 1):
        print("| " + f"{i}. {quest['name']}".ljust(24) + " |")
    
    print("+" + "-" * 26 + "+")

def display_condition_diagram(hero, quest_name="Defeat Goblin"):
    """
    Displays the nested conditional logic diagram for the selected quest
    """
    print("\n+" + "-" * 26 + "+")
    print("|" + "Player's Current State".center(26) + "|")
    print("+" + "-" * 26 + "+")
    print("| " + f"Location: {hero.current_location.capitalize()}".ljust(24) + " |")
    print("| " + f"Inventory: {', '.join(hero.inventory)}".ljust(24) + " |")
    print("| " + f"Strength: {hero.combat_strength}".ljust(24) + " |")
    print("+" + "-" * 26 + "+")
    
    if quest_name == "Defeat Goblin":
        print("|" + "↓".center(26) + "|")
        print("+" + "-" * 26 + "+")
        print("| " + f"Is player in correct".ljust(24) + " |")
        print("| " + f"location? (Forest)".ljust(24) + " |")
        print("+" + "-" * 26 + "+")
        
        print("|".center(28))
        print("+" + "-" * 10 + "+" + "-" * 10 + "+")
        print("|" + "No".center(10) + "|" + "Yes".center(10) + "|")
        print("+" + "-" * 10 + "+" + "-" * 10 + "+")
        
        print("↓".center(12) + "↓".center(16))
        print('"Wrong location"'.center(12) + "+" + "-" * 26 + "+")
        print(" " * 12 + "| " + "Does player have a".ljust(24) + " |")
        print(" " * 12 + "| " + "magic sword?".ljust(24) + " |")
        print(" " * 12 + "+" + "-" * 26 + "+")
        
        print(" " * 12 + "|".center(28))
        print(" " * 12 + "+" + "-" * 10 + "+" + "-" * 10 + "+")
        print(" " * 12 + "|" + "No".center(10) + "|" + "Yes".center(10) + "|")
        print(" " * 12 + "+" + "-" * 10 + "+" + "-" * 10 + "+")
        
        print(" " * 12 + "↓".center(12) + "↓".center(16))
        print(" " * 12 + "+" + "-" * 16 + "+" + '"Can fight Forest Guardian!"')
        print(" " * 12 + "| " + "Is strength > 7?".ljust(14) + " |")
        print(" " * 12 + "+" + "-" * 16 + "+")
        
        print(" " * 12 + "|".center(18))
        print(" " * 12 + "+" + "-" * 8 + "+" + "-" * 8 + "+")
        print(" " * 12 + "|" + "No".center(8) + "|" + "Yes".center(8) + "|")
        print(" " * 12 + "+" + "-" * 8 + "+" + "-" * 8 + "+")
        
        print(" " * 12 + "↓".center(10) + "↓".center(10))
        print('"Need more power or sword"' + " " * 2 + '"Can fight with brute strength!"')

# Main code starts here
print(f"Operating System: {os.name}")
print(f"Python Version: {platform.python_version()}")

hero = Hero()
monster = Monster()

# Load quest progress
hero.completed_quests = functions.load_quest_progress("Player1")

# Give player some starter items
hero.add_to_inventory("map")
hero.add_to_inventory("health potion")

print("\n=== WELCOME TO THE ADVENTURE GAME ===\n")

while True:
    print("\n=== MAIN MENU ===")
    print("1. Battle Monster")
    print("2. View Available Quests")
    print("3. Travel to Location")
    print("4. View Hero Status")
    print("5. Exit Game")
    
    choice = input("Choose an option (1-5): ").strip()
    
    if choice == "1":
        # Original battle system
        num_dream_lvls = -1
        while num_dream_lvls < 0 or num_dream_lvls > 3:
            try:
                num_dream_lvls = int(input("How many dream levels do you want to go down? (Enter 0-3): "))
                if num_dream_lvls < 0 or num_dream_lvls > 3:
                    raise ValueError("Number must be between 0 and 3.")
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

        print("Battle Begins!")
        while hero.health_points > 0 and monster.health_points > 0:
            hero.hero_attacks(monster)
            time.sleep(1)  # Add a delay after the hero's attack
            if monster.health_points > 0:
                monster.monster_attacks(hero)
                time.sleep(1)  # Add a delay after the monster's attack

        winner = "Hero" if hero.health_points > 0 else "Monster"
        functions.save_game(winner, "Player1", 3)
        print(f"{winner} wins!")
        
        # Reset monster for next battle
        if winner == "Hero":
            hero.gain_xp(5)  # Gain XP for winning
            monster = Monster()  # Create a new monster
        else:
            # Game over - restart with new hero
            print("Game Over! Starting a new adventure...")
            hero = Hero()
            monster = Monster()
            hero.completed_quests = functions.load_quest_progress("Player1")
            hero.add_to_inventory("map")
            hero.add_to_inventory("health potion")
    
    elif choice == "2":
        # Quest system
        print(f"\nCurrent location: {hero.current_location}")
        
        # Show quest diagrams
        display_quest_diagram(hero)
        
        available_quests = hero.view_available_quests()
        
        if available_quests:
            # Show conditional diagram for Defeat Goblin
            display_condition_diagram(hero)
            
            quest_choice = input("\nSelect a quest number (or 0 to cancel): ")
            try:
                quest_index = int(quest_choice) - 1
                if quest_index >= 0:
                    if hero.start_quest(quest_index, available_quests):
                        print("\nQuest started! You can now:")
                        print("1. Try to complete the quest")
                        print("2. Abandon the quest")
                        
                        quest_action = input("Choose an option (1-2): ").strip()
                        if quest_action == "1":
                            # Simple simulation of quest completion
                            print("Attempting to complete quest...")
                            time.sleep(2)
                            success_chance = random.random()
                            if success_chance > 0.3:  # 70% chance of success
                                hero.complete_active_quest()
                            else:
                                print("Failed to complete the quest!")
                                hero.active_quest = None
            except ValueError:
                print("Invalid selection.")
    
    elif choice == "3":
        # Travel system
        print("\nAvailable locations:")
        locations = ["town", "forest", "cave", "mountain", "village"]
        for i, location in enumerate(locations):
            print(f"{i+1}. {location.capitalize()}")
        
        try:
            location_choice = int(input("\nSelect a location number: ")) - 1
            if 0 <= location_choice < len(locations):
                hero.change_location(locations[location_choice])
            else:
                print("Invalid location selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    elif choice == "4":
        # View hero status
        print("\n=== HERO STATUS ===")
        print(f"Level: {hero.level}")
        print(f"XP: {hero.xp}")
        print(f"Health: {hero.health_points}")
        print(f"Combat Strength: {hero.combat_strength}")
        print(f"Current Location: {hero.current_location}")
        print(f"Inventory: {', '.join(hero.inventory) if hero.inventory else 'Empty'}")
        print(f"Completed Quests: {len(hero.completed_quests)}")
        if hero.active_quest:
            print(f"Active Quest: {hero.active_quest['name']}")
    
    elif choice == "5":
        print("Thanks for playing!")
        break
    
    else:
        print("Invalid choice. Please select a number between 1 and 5.")
