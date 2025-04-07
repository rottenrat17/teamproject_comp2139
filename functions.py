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