from common.agent import Agent

class NPCAgent(Agent):
    def __init__(self):
        super().__init__(
                name="NPC",
                description="The agent that acts as a non-player character in the story. Whenever the interaction of one non-player character is required, the orchestrator agent will call this agent with the appropriate context and personality, and this agent will generate the response and/or action as if it were that character.",
                tools=[]
            )
        
    