import os
from common.openai_client import get_openai_client
from common.logging import config_logging

cuur_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
class Agent:
    def __init__(self, name: str, description: str, tools: list = [], threading: bool = True):
        openai_client = get_openai_client()
        with open(f'{cuur_dir}/prompts/{name}.md', 'r') as f:
            instructions = f.read()
        self.name = name
        self.description = description
        self.agent = openai_client.create_agent(
                        name=name,
                        description=description,
                        instructions=instructions,
                        tools=tools
                    )
        if threading:
            self.thread = self.agent.get_new_thread()
        else:
            self.thread = None
            
        self.logger = config_logging(self.name)
        
    async def run(self, input: str) -> str:
        self.logger.info(f"Received input: {input}")
        response = await self.agent.run(input, thread=self.thread)
        self.logger.info(f"Generated response: {response.text}")
        return response.text