# COMP2152 Team Project

## Saeed's Feature: Dynamic Quest System

This implementation adds a Dynamic Quest System to the Hero vs Monster game, allowing players to take on quests based on their dream level and hero strength.

### Features:
- Quests of varying difficulty and rewards
- List comprehension to filter available quests based on player level and strength
- Nested conditional statements to determine if a player can start a quest
- Inventory system to collect and use items required for quests
- Random quest generation
- Save/load quest progress

### Implementation Details:
- Created a separate `Quest` class to represent individual quests with attributes like difficulty, rewards, and requirements
- Used a `QuestSystem` class to manage all quest-related functionality
- Integrated quest system with the main game loop
- Extended the Hero class to track dream level for quest compatibility

### Code Highlights:
- List comprehension for filtering available quests:
```python
return [quest for quest in self.available_quests 
        if quest.location <= dream_level
        and not quest.completed
        and quest.difficulty <= hero_strength + 2]
```

- Nested conditionals for quest eligibility:
```python
if quest in self.available_quests and not quest.completed:
    if quest.location <= hero.dream_level:
        if quest.required_items:
            for item in quest.required_items:
                if item not in self.player_inventory:
                    return False
            return True
        else:
            return True
``` 