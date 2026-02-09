from common.agent import Agent
try:
    from agent_framework import tool
except ImportError:
    from agent_framework import ai_function
    tool = ai_function        

class OrchestratorAgent(Agent):
    def __init__(self, orchestrated_agents: list):
        super().__init__(
                name="Orchestrator",
                description="The agent that narrates the story based on the user input and the story context.",
                tools=[tool(agent.run, name=agent.name, description=agent.description) for agent in orchestrated_agents]
            )