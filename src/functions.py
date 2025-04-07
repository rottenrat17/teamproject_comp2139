import random
import os

def roll_dice():
    """
    Roll a 6-sided die
    """
    return random.randint(1, 6)

def save_game(hero, monsters_killed=0):
    """
    Save the game progress to a file
    Note: This simplified save system doesn't save inventory items
    """
    with open("save.txt", "w") as file:
        file.write(str(hero.health_points) + "\n")
        file.write(str(monsters_killed) + "\n")
        file.write(str(hero.combat_strength) + "\n")
        file.write(str(hero.level) + "\n")
        file.write(str(hero.experience) + "\n")
    
    print("Game saved successfully!")

def load_game():
    """
    Load the game progress from a file
    Note: This simplified load system doesn't restore inventory items
    """
    try:
        with open("save.txt", "r") as file:
            lines = file.readlines()
            health_points = int(lines[0].strip())
            
            # Get monsters killed if available
            monsters_killed = 0
            if len(lines) > 1:
                monsters_killed = int(lines[1].strip())
            
            # Load additional attributes if available
            combat_strength = None
            level = 1
            experience = 0
            
            if len(lines) > 2:
                combat_strength = int(lines[2].strip())
            
            if len(lines) > 3:
                level = int(lines[3].strip())
            
            if len(lines) > 4:
                experience = int(lines[4].strip())
            
            return health_points, monsters_killed, combat_strength, level, experience
    except FileNotFoundError:
        print("No save file found.")
        return None, 0, None, 1, 0
    except Exception as e:
        print(f"Error loading game: {e}")
        return None, 0, None, 1, 0

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