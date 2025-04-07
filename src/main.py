import os
import platform
import random
from functions import roll_dice, save_game, load_game, dream_levels
from hero import Hero
from monster import Monster
from loot import LootSystem

# Print Python version and OS information
print(f"Python Version: {platform.python_version()}")
print(f"Operating System: {os.name}")

# Initialize the loot system
loot_system = LootSystem()

def use_inventory_item(hero):
    """
    Allow the hero to use an item from their inventory
    """
    if not hero.inventory:
        print("Inventory is empty! Nothing to use.")
        return False
    
    hero.show_inventory()
    
    while True:
        try:
            choice = input("Enter item number to use (or 0 to cancel): ")
            
            # Check if user wants to cancel
            if choice == "0":
                return False
            
            item_index = int(choice) - 1
            
            if 0 <= item_index < len(hero.inventory):
                # Get selected item and remove from inventory
                selected_item = hero.inventory.pop(item_index)
                print(f"Using {selected_item.name}...")
                
                # Apply item effect
                loot_system.apply_item_effect(hero, selected_item)
                
                return True
            else:
                print(f"Invalid selection. Please enter 0 to cancel or a number between 1 and {len(hero.inventory)}")
        except ValueError:
            print("Please enter a valid number (0 to cancel).")

# Testing Functions
def fight_monster(hero, monster, monsters_killed=0):
    """
    Run a fight sequence between hero and monster
    """
    print("\n--- Fight Begins ---")
    print(f"Hero Health: {hero.health_points}, Combat Strength: {hero.combat_strength}, Level: {hero.level}")
    print(f"Monster Health: {monster.m_health_points}, Combat Strength: {monster.m_combat_strength}")
    
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
            
            # Award experience to hero - 20 exp per monster
            hero.gain_experience(20)
            print(f"Hero gained 20 experience. Total: {hero.experience}")
            
            # Check for item drops using the loot system
            dropped_item = loot_system.get_loot(monster, hero.level)
            if dropped_item:
                print(f"\nThe monster dropped: {dropped_item}")
                use_item = input("Do you want to use this item? (y/n): ")
                if use_item.lower() == "y":
                    loot_system.apply_item_effect(hero, dropped_item)
                else:
                    hero.add_to_inventory(dropped_item)
            
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

def main():
    """
    Main game loop
    """
    print("\nWelcome to the Hero vs Monster Game!")
    print("NEW FEATURE: Monster Loot System - Defeat monsters for a chance to get equipment!")
    
    # Initialize variables
    monsters_killed = 0
    loaded_health = None
    loaded_combat = None
    loaded_level = None
    loaded_exp = None
    
    # Load game if available
    load_option = input("Do you want to load a saved game? (y/n): ")
    if load_option.lower() == "y":
        loaded_health, monsters_killed, loaded_combat, loaded_level, loaded_exp = load_game()
    
    # Create hero object
    hero = Hero()
    
    # Set hero attributes from saved game if available
    if loaded_health:
        hero.health_points = loaded_health
    if loaded_combat:
        hero.combat_strength = loaded_combat
    if loaded_level:
        hero.level = loaded_level
    if loaded_exp:
        hero.experience = loaded_exp
    
    while hero.health_points > 0:
        # Show hero inventory
        show_inventory = input("Do you want to see your inventory? (y/n): ")
        if show_inventory.lower() == "y":
            hero.show_inventory()
            
            # Automatically offer to use items if inventory is not empty
            if hero.inventory:
                use_inventory_item(hero)
        
        # Ask for dream level
        dream_level = dream_levels()
        print(f"Dream Level selected: {dream_level}")
        
        # Create monster object
        monster = Monster()
        
        # Fight sequence
        victory, monsters_killed = fight_monster(hero, monster, monsters_killed)
        
        # Game over if hero is defeated
        if not victory:
            print("\nGame Over! The hero has fallen.")
            break
        
        # Option to save and continue
        save_option = input("\nDo you want to save the game? (y/n): ")
        if save_option.lower() == "y":
            save_game(hero, monsters_killed)
        
        continue_option = input("Do you want to fight another monster? (y/n): ")
        if continue_option.lower() != "y":
            print("Thanks for playing!")
            break
    
    print(f"\nTotal monsters killed: {monsters_killed}")
    print(f"Hero reached level: {hero.level}")
    print(f"Final hero stats - Health: {hero.health_points}, Combat Strength: {hero.combat_strength}")

if __name__ == "__main__":
    main() 