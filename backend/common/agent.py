import os
from common.openai_client import get_openai_client
from common.logging import config_logging
from agent_framework import ChatAgent
import json

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
class Agent:
    def __init__(self, name: str, description: str, tools: list = [], threading: bool = True):
        openai_client = get_openai_client()
        self.name = name
        self.description = description
        
        self.logger = config_logging(self.name)
        try:
            with open(f'{root_dir}/prompts/{name}.md', 'r') as f:
                instructions = f.read()
        except FileNotFoundError:
            instructions = "No instructions provided."
            self.logger.error(f"No instructions found") 

        self.agent = ChatAgent(
            chat_client=openai_client,
            name=name,
            description=description,
            instructions=instructions,
            tools=tools
        )
        if threading:
            self.thread = self.agent.get_new_thread()
        else:
            self.thread = None
        
    async def run(self, input: str) -> str:
        self.logger.info(f"Received input: {input}")
        response = await self.agent.run(input, thread=self.thread)
        self.logger.info(f"Generated response: {response.text}")
        self.logger.info(f"Usage details: {response.usage_details}")
        return response.text