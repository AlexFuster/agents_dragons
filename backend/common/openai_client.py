from agent_framework.azure import AzureOpenAIChatClient
from common.config import Config

def get_openai_client() -> AzureOpenAIChatClient:
    openai_client = AzureOpenAIChatClient(api_key=Config.openai_key, deployment_name=Config.openai_deployment, endpoint=Config.openai_api_base)
    return openai_client