from common.agent import Agent
from common.models import Scene  

class OrchestratorAgent(Agent):
    def __init__(self, tools: list):
        super().__init__(
                name="Orchestrator",
                description="The agent that narrates the story based on the user input and the story context.",
                tools=tools,
                parallel_tool_calls=False,
                allow_multiple_tool_calls=False
            )
        
    def run(self, user_input: str, scene: Scene) -> str:
        full_input = f"Current scene: {scene}\n\nUser input: {user_input}"
        return super().run(full_input)