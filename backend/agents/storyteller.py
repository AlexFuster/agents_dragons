from common.agent import Agent

class StorytellerAgent(Agent):
    def __init__(self):
        super().__init__(
                name="Storyteller",
                description="The agent that narrates the story based on the user input and the story context.",
                tools=[]
            )