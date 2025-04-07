import random
import os

def roll_dice():
    """
    Roll a 6-sided die
    """
    return random.randint(1, 6)

def save_game(health_points, monsters_killed=0):
    """
    Save the game progress to a file
    """
    with open("save.txt", "w") as file:
        file.write(str(health_points) + "\n")
        file.write(str(monsters_killed) + "\n")
    
    print("Game saved successfully!")

def load_game():
    """
    Load the game progress from a file
    """
    try:
        with open("save.txt", "r") as file:
            lines = file.readlines()
            health_points = int(lines[0].strip())
            
            # Get monsters killed if available
            monsters_killed = 0
            if len(lines) > 1:
                monsters_killed = int(lines[1].strip())
            
            return health_points, monsters_killed
    except FileNotFoundError:
        print("No save file found.")
        return None, 0
    except Exception as e:
        print(f"Error loading game: {e}")
        return None, 0

def dream_levels():
    """
    Get dream level from user with validation
    """
    while True:
        try:
            level = int(input("Enter dream level (0-3): "))
            if 0 <= level <= 3:
                return level
            else:
                print("Dream level must be between 0 and 3.")
        except ValueError:
            print("Please enter a valid integer.")

def get_random_weather():
    """
    Generate a random weather condition
    """
    weathers = ["Sunny", "Rainy", "Foggy", "Stormy"]
    return random.choice(weathers)

def get_weather_effects(weather):
    """
    Return the effects of the current weather
    """
    weather_effects = {
        "Sunny": {"name": "Boost Fire", "hero_effect": 2, "monster_effect": 1},
        "Rainy": {"name": "Slow Movement", "hero_effect": -1, "monster_effect": -1},
        "Foggy": {"name": "Low Visibility", "hero_effect": -2, "monster_effect": -2},
        "Stormy": {"name": "Electric Buff", "hero_effect": 3, "monster_effect": 2}
    }
    return weather_effects.get(weather, {"name": "Normal", "hero_effect": 0, "monster_effect": 0})

def display_weather_info(weather):
    """
    Display current weather and its effects
    """
    effects = get_weather_effects(weather)
    
    print("+------------------------------+")
    print(f"| Active Weather: {weather.ljust(12)} |")
    print(f"| Effects: {effects['name'].ljust(16)} |")
    print("+------------------------------+")
    
    print("\nWeather Effects:")
    if weather == "Sunny":
        print("  - Fire attacks are boosted")
    elif weather == "Rainy":
        print("  - Movement is slower")
    elif weather == "Foggy":
        print("  - Accuracy is reduced")
    elif weather == "Stormy":
        print("  - Electric attacks get a buff")
    print() 