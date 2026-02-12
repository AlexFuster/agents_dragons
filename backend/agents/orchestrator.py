from common.agent import Agent
from agent_framework import AIFunction    

class OrchestratorAgent(Agent):
    def __init__(self, orchestrated_agents: list):
        super().__init__(
                name="Orchestrator",
                description="The agent that narrates the story based on the user input and the story context.",
                tools=[AIFunction(func=agent.run, name=agent.name, description=agent.description, input_model=agent.input_model) for agent in orchestrated_agents],
                parallel_tool_calls=False,
                allow_multiple_tool_calls=False
            )