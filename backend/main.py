from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.npc import NPCAgent
from agents.orchestrator import OrchestratorAgent
from agents.rules import RulesAgent
from agents.scene import SceneManager
import uvicorn
import logging
from agent_framework import AIFunction    



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
tools = [AIFunction(func=agent.run, name=agent.name, description=agent.description, input_model=agent.input_model) for agent in sub_agents]

scene_manager = SceneManager()
scene_tools = [AIFunction(func=getattr(scene_manager, tool['name']), name=tool['name'], description=tool['description'], input_model=tool['input_model']) for tool in scene_manager.tools_exposed]
tools.extend(scene_tools)

orchestrator_agent = OrchestratorAgent(tools=tools)


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
        scene = scene_manager.get_scene()  # Get the current scene to provide context to the orchestrator
        result = await orchestrator_agent.run(request.message, scene)
    else:
        selected_agent = next(agent for agent in sub_agents if agent.name == request.agent_name)
        logging.info(f"Received message for {request.agent_name}: {request.message}")
        result = await selected_agent.run(request.message)
        
    result = result.replace("```markdown", "").replace("```", "")  # Clean markdown code block formatting if present
    return GameResponse(response=result)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)