from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.npc import NPCAgent
from agents.orchestrator import OrchestratorAgent
from agents.rules import RulesAgent
import uvicorn
import logging



app = FastAPI(title="Agents & Dragons API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize agents
sub_agents = [NPCAgent(), RulesAgent()]
orchestrator_agent = OrchestratorAgent(orchestrated_agents=sub_agents)


class GameRequest(BaseModel):
    message: str
    agent_name: str = "Orchestrator"


class GameResponse(BaseModel):
    response: str


@app.post("/game", response_model=GameResponse)
async def play_game(request: GameRequest):
    """
    Send a message to the orchestrator agent and get a response.
    """
    if request.agent_name == "Orchestrator":
        logging.info(f"Received message for Orchestrator: {request.message}")
        result = await orchestrator_agent.run(request.message)
    else:
        selected_agent = next(agent for agent in sub_agents if agent.name == request.agent_name)
        logging.info(f"Received message for {request.agent_name}: {request.message}")
        result = await selected_agent.run(request.message)
        
    result = result.replace("```markdown", "").replace("```", "")  # Clean markdown code block formatting if present
    return GameResponse(response=result)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)