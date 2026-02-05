import dotenv
import os

dotenv.load_dotenv()

class Config:
    openai_key: str = os.getenv("OPENAI_KEY")
    openai_deployment: str = os.getenv("OPENAI_DEPLOYMENT")
    openai_api_base: str = os.getenv("OPENAI_API_BASE")