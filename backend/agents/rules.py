import random
from common.agent import Agent


def simulate_check(difficulty: int, modifier: int) -> bool:
    """
    Simulates a D20 skill check or attack check.
    
    Args:
        difficulty: The difficulty class (DC) of the check
        modifier: The modifier to add to the dice roll
        
    Returns:
        True if the check succeeds (roll + modifier >= difficulty), False otherwise
    """
    dice_roll = random.randint(1, 20)
    total = dice_roll + modifier
    return total >= difficulty


def roll_dice(num_dice: int, dice_type: int, modifier: int = 0) -> int:
    """
    Rolls multiple dice of the same type and adds a flat modifier.
    
    Supports dice types: D4, D6, D8, D10, D12, D20, D100
    Example: roll_dice(2, 6, 3) simulates 2D6+3
    
    Args:
        num_dice: The number of dice to roll
        dice_type: The type of dice (4, 6, 8, 10, 12, 20, or 100)
        modifier: The flat modifier to add to the total (default: 0)
        
    Returns:
        The total sum of all dice rolls plus the modifier
        
    Raises:
        ValueError: If dice_type is not supported
    """
    valid_dice = [4, 6, 8, 10, 12, 20, 100]
    if dice_type not in valid_dice:
        raise ValueError(f"Unsupported dice type: D{dice_type}. Valid types: {valid_dice}")
    
    total = sum(random.randint(1, dice_type) for _ in range(num_dice))
    return total + modifier


class RulesAgent(Agent):
    def __init__(self):
        super().__init__(
                name="Rules",
                description="This agent has access to the rules of the story world. It receives the intent of the characters, checks if it is possible and how difficult it is. It returns what happens with the action the character actions",
                tools=[simulate_check, roll_dice]
            )
        # Force JSON response format
        self.agent.response_format = {"type": "json_object"}
        
    def run(self, input: str, story_context: str, character_personality: str) -> str:
        full_input = f"{input}\n\nStory context: {story_context}\n\nYour personality: {character_personality}"
        return super().run(full_input)
        
    