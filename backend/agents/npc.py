from common.agent import Agent
from common.models import NPCOutput

class NPCAgent(Agent):
    def __init__(self):
        super().__init__(
                name="NPC",
                description="""
                    The agent that acts as a single non-player character in the story. 
                    Whenever the interaction of one non-player character is required, the orchestrator agent will call this agent with the appropriate context, name and personality, and this agent will generate the response and/or action intent as if it were that character.
                """,
                tools=[]
            )
        
    async def run(self, story_context: str, character_name: str, character_personality: str) -> str:
        full_input = f"Story context: {story_context}\n\nYour name: {character_name}\nYour personality: {character_personality}"
        return await super().run(full_input, response_format=NPCOutput)
        
    