import os
import platform
import random
from functions import roll_dice, save_game, load_game, dream_levels, get_random_weather, display_weather_info
from hero import Hero
from monster import Monster

# Print Python version and OS information
print(f"Python Version: {platform.python_version()}")
print(f"Operating System: {os.name}")

# Testing Functions
def fight_monster(hero, monster, monsters_killed=0):
    """
    Run a fight sequence between hero and monster
    """
    # Generate random weather for this fight
    current_weather = get_random_weather()
    print("\n--- Weather System ---")
    display_weather_info(current_weather)
    
    print("\n--- Fight Begins ---")
    print(f"Hero Health: {hero.health_points}, Combat Strength: {hero.combat_strength}")
    print(f"Monster Health: {monster.m_health_points}, Combat Strength: {monster.m_combat_strength}")
    
    round_count = 1
    
    while hero.health_points > 0 and monster.m_health_points > 0:
        print(f"\nRound {round_count}")
        
        # Hero attacks monster with weather effects
        hero_attack = hero.hero_attacks(current_weather)
        monster.m_health_points -= hero_attack
        print(f"Hero attacks for {hero_attack} damage. Monster health: {max(0, monster.m_health_points)}")
        
        # Check if monster is defeated
        if monster.m_health_points <= 0:
            print("Monster has been defeated!")
            monsters_killed += 1
            break
        
        # Monster attacks hero with weather effects
        monster_attack = monster.monster_attacks(current_weather)
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
    
    # Initialize variables
    monsters_killed = 0
    loaded_health = None
    
    # Load game if available
    load_option = input("Do you want to load a saved game? (y/n): ")
    if load_option.lower() == "y":
        loaded_health, monsters_killed = load_game()
    
    # Create hero object
    hero = Hero()
    
    # Set hero health from saved game if available
    if loaded_health:
        hero.health_points = loaded_health
    
    while hero.health_points > 0:
        # Ask for dream level
        dream_level = dream_levels()
        print(f"Dream Level selected: {dream_level}")
        
        # Generate weather for this encounter
        current_weather = get_random_weather()
        print("\n--- Current Weather Conditions ---")
        display_weather_info(current_weather)
        
        # Ask player if they want to proceed with current weather
        weather_choice = input("Do you want to fight in the current weather? (y/n): ")
        
        # If player doesn't like the weather, they can try for a new one
        while weather_choice.lower() != "y":
            print("\nYou decide to wait for weather conditions to change...")
            current_weather = get_random_weather()
            print("\n--- New Weather Conditions ---")
            display_weather_info(current_weather)
            weather_choice = input("Do you want to fight in this weather? (y/n): ")
        
        # Create monster object
        monster = Monster()
        
        # Fight sequence with current weather
        victory, monsters_killed = fight_monster(hero, monster, monsters_killed)
        
        # Game over if hero is defeated
        if not victory:
            print("\nGame Over! The hero has fallen.")
            break
        
        # Option to save and continue
        save_option = input("\nDo you want to save the game? (y/n): ")
        if save_option.lower() == "y":
            save_game(hero.health_points, monsters_killed)
        
        continue_option = input("Do you want to fight another monster? (y/n): ")
        if continue_option.lower() != "y":
            print("Thanks for playing!")
            break
    
    print(f"\nTotal monsters killed: {monsters_killed}")

if __name__ == "__main__":
    main() 