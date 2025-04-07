import os
import platform
import random
from functions import roll_dice, save_game, load_game, dream_levels
from hero import Hero
from monster import Monster
from quest_system import QuestSystem, Quest
from companion import Companion  # Import the new Companion class

# Print Python version and OS information
print(f"Python Version: {platform.python_version()}")
print(f"Operating System: {os.name}")

# Define available companions
available_companions = [
    Companion("Luna", "Healer"),
    Companion("Brutus", "Fighter"),
    Companion("Aegis", "Guardian"),
    Companion("Mystic", "Mage")
]

# Testing Functions
def fight_monster(hero, monster, monsters_killed=0):
    """
    Run a fight sequence between hero and monster
    """
    print("\n--- Fight Begins ---")
    print(f"Hero Health: {hero.health_points}, Combat Strength: {hero.combat_strength}")
    print(f"Monster Health: {monster.m_health_points}, Combat Strength: {monster.m_combat_strength}")
    
    # Allow hero to use companion ability before the fight if they have one
    if hero.companion:
        use_companion = input(f"Do you want {hero.companion.name} to assist you? (y/n): ")
        if use_companion.lower() == 'y':
            hero.use_companion_ability()
            print(f"Updated Hero stats - Health: {hero.health_points}, Combat Strength: {hero.combat_strength}")
    
    round_count = 1
    
    while hero.health_points > 0 and monster.m_health_points > 0:
        print(f"\nRound {round_count}")
        
        # Hero attacks monster
        hero_attack = hero.hero_attacks()
        monster.m_health_points -= hero_attack
        print(f"Hero attacks for {hero_attack} damage. Monster health: {max(0, monster.m_health_points)}")
        
        # Check if monster is defeated
        if monster.m_health_points <= 0:
            print("Monster has been defeated!")
            monsters_killed += 1
            break
        
        # Monster attacks hero
        monster_attack = monster.monster_attacks()
        hero.health_points -= monster_attack
        print(f"Monster attacks for {monster_attack} damage. Hero health: {max(0, hero.health_points)}")
        
        # Check if hero is defeated
        if hero.health_points <= 0:
            print("Hero has been defeated!")
            break
        
        round_count += 1
    
    print("--- Fight Ends ---")
    return hero.health_points > 0, monsters_killed

def handle_quests(hero, quest_system):
    """
    Handle the quest system interaction
    """
    while True:
        print("\n--- Quest Menu ---")
        print("1. View available quests")
        print("2. View inventory")
        print("3. View completed quests")
        print("4. Find a random quest")
        print("5. Add test item to inventory")
        print("0. Return to main game")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            # Use list comprehension to get available quests
            available_quests = quest_system.get_available_quests(hero.dream_level, hero.combat_strength)
            
            if not available_quests:
                print("No quests available for your current dream level and strength.")
                continue
            
            print("\nAvailable Quests:")
            for i, quest in enumerate(available_quests):
                print(f"{i+1}. {quest}")
            
            quest_choice = input("\nSelect a quest number to start (or 0 to cancel): ")
            try:
                quest_idx = int(quest_choice) - 1
                if quest_idx < 0:
                    continue
                    
                selected_quest = available_quests[quest_idx]
                
                # Use nested conditionals to check if player can start the quest
                if quest_system.can_start_quest(selected_quest, hero):
                    print(f"\nStarting quest: {selected_quest.name}")
                    print(f"Description: {selected_quest.description}")
                    
                    # Simple quest completion simulation
                    success_chance = min(90, max(10, (hero.combat_strength * 10) - (selected_quest.difficulty * 10) + 50))
                    print(f"Quest difficulty: {selected_quest.difficulty}, Your strength: {hero.combat_strength}")
                    print(f"Success chance: {success_chance}%")
                    
                    proceed = input("Do you want to proceed with this quest? (y/n): ")
                    if proceed.lower() == "y":
                        if random.randint(1, 100) <= success_chance:
                            print(f"\nSuccess! You completed the quest: {selected_quest.name}")
                            quest_system.complete_quest(selected_quest, hero)
                        else:
                            damage = selected_quest.difficulty * 2
                            hero.health_points -= damage
                            print(f"\nYou failed the quest and took {damage} damage!")
                            if hero.health_points <= 0:
                                print("The quest was too difficult and you have been defeated!")
                                return False
            except (ValueError, IndexError):
                print("Invalid choice.")
                
        elif choice == "2":
            print("\nInventory:")
            if not quest_system.player_inventory:
                print("Your inventory is empty.")
            else:
                for i, item in enumerate(quest_system.player_inventory):
                    print(f"{i+1}. {item}")
                    
        elif choice == "3":
            print("\nCompleted Quests:")
            if not quest_system.completed_quests:
                print("You haven't completed any quests yet.")
            else:
                for i, quest in enumerate(quest_system.completed_quests):
                    print(f"{i+1}. {quest}")
                    
        elif choice == "4":
            random_quest = quest_system.generate_random_quest(hero.dream_level)
            quest_system.available_quests.append(random_quest)
            print(f"\nNew quest discovered: {random_quest}")
            
        elif choice == "5":
            items = ["sword", "lantern", "potion", "key", "map", "compass", "courage", "meditation"]
            item = random.choice(items)
            quest_system.add_item_to_inventory(item)
            
        elif choice == "0":
            return True
    
    return True

def handle_companion(hero):
    """
    Handle companion selection and abilities
    """
    while True:
        print("\n--- Companion Menu ---")
        print(f"Current companion: {hero.companion.name if hero.companion else 'None'}")
        print("1. Choose a companion")
        print("2. View companion details")
        print("3. Use companion ability")
        print("0. Return to main game")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            print("\nAvailable Companions:")
            for i, companion in enumerate(available_companions):
                print(f"{i+1}. {companion.name} - {companion.role.capitalize()}")
            
            companion_choice = input("\nSelect a companion number (or 0 to cancel): ")
            try:
                companion_idx = int(companion_choice) - 1
                if companion_idx < 0:
                    continue
                    
                selected_companion = available_companions[companion_idx]
                hero.set_companion(selected_companion)
            except (ValueError, IndexError):
                print("Invalid choice.")
                
        elif choice == "2":
            if hero.companion:
                print(f"\nCompanion: {hero.companion.name}")
                print(f"Role: {hero.companion.role.capitalize()}")
                print(f"Power: {hero.companion.power}")
                
                if hero.companion.role == "healer":
                    print(f"Ability: Heals {hero.name} for {hero.companion.power} HP")
                elif hero.companion.role == "fighter":
                    print(f"Ability: Boosts {hero.name}'s attack by {hero.companion.power}")
                elif hero.companion.role == "guardian":
                    print(f"Ability: Provides +2 HP and +1 attack bonus")
                else:
                    print("Ability: Unknown")
            else:
                print("You don't have a companion yet.")
                
        elif choice == "3":
            if hero.companion:
                hero.use_companion_ability()
            else:
                print("You don't have a companion to use an ability.")
                
        elif choice == "0":
            return

def main():
    """
    Main game loop
    """
    print("\nWelcome to the Hero vs Monster Game with Dynamic Quest System and Companion Support!")
    
    # Initialize variables
    monsters_killed = 0
    loaded_health = None
    
    # Initialize quest system
    quest_system = QuestSystem()
    
    # Get player name
    player_name = input("Enter your hero's name (or press Enter for default): ")
    
    # Load game if available
    load_option = input("Do you want to load a saved game? (y/n): ")
    if load_option.lower() == "y":
        loaded_health, monsters_killed = load_game()
        quest_system.load_quest_progress()
    
    # Create hero object
    hero = Hero(player_name if player_name else "Adventurer")
    
    # Set hero health from saved game if available
    if loaded_health:
        hero.health_points = loaded_health
    
    # Choose initial companion
    print("\n--- Choose Your Starting Companion ---")
    print("A companion will aid you in your journey!")
    for i, companion in enumerate(available_companions):
        print(f"{i+1}. {companion.name} - {companion.role.capitalize()}")
    
    companion_choice = input("\nSelect a companion number (or 0 to journey alone): ")
    try:
        companion_idx = int(companion_choice) - 1
        if companion_idx >= 0:
            selected_companion = available_companions[companion_idx]
            hero.set_companion(selected_companion)
    except (ValueError, IndexError):
        print("Invalid choice. You'll start your journey alone.")
    
    while hero.health_points > 0:
        print("\n--- Main Menu ---")
        print(f"Hero: {hero.name} - Health: {hero.health_points}, Combat Strength: {hero.combat_strength}")
        if hero.companion:
            print(f"Companion: {hero.companion.name} the {hero.companion.role.capitalize()}")
        print("1. Enter a dream level")
        print("2. Access quest system")
        print("3. Manage companion")
        print("4. Save game")
        print("5. Quit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            # Ask for dream level
            dream_level = dream_levels()
            print(f"Dream Level selected: {dream_level}")
            hero.set_dream_level(dream_level)
            
            # Create monster object
            monster = Monster()
            
            # Fight sequence
            victory, monsters_killed = fight_monster(hero, monster, monsters_killed)
            
            # Game over if hero is defeated
            if not victory:
                print("\nGame Over! The hero has fallen.")
                break
            
        elif choice == "2":
            # Access quest system
            if not handle_quests(hero, quest_system):
                print("\nGame Over! The hero has fallen during a quest.")
                break
                
        elif choice == "3":
            # Access companion system
            handle_companion(hero)
            
        elif choice == "4":
            # Save game
            save_game(hero.health_points, monsters_killed)
            quest_system.save_quest_progress()
            
        elif choice == "5":
            print("Thanks for playing!")
            break
    
    print(f"\nTotal monsters killed: {monsters_killed}")
    print(f"Total quests completed: {len(quest_system.completed_quests)}")

if __name__ == "__main__":
    main() 