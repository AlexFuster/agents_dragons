from pydantic import BaseModel, Field
from typing import List, Literal


class SceneCharacter(BaseModel):
    name: str
    type: str
    physical_description: str
    personality_description: str
    current_hp: int = Field(ge=0)
    distance_to_pj: Literal["none", "close", "near", "far"]
    is_pj: bool
    attitude_to_pj: Literal["pos", "neg", "neutral"]
    
class SceneAddInput(BaseModel):
    character: SceneCharacter
    
class SceneUpdateInput(BaseModel):
    name: str
    keys_to_update: List[str]
    new_values: List[str | int | bool]
    
class SceneRemoveInput(BaseModel):
    name: str
    
class Scene(BaseModel):
    characters: List[SceneCharacter]

class Stats(BaseModel):
    STR: int
    DEX: int
    CON: int
    INT: int
    WIS: int
    CHA: int
    AC: int
    DMG_DICE: int

class RulesCharacter(BaseModel):
    name: str
    intent_list: List[str]
    stats: Stats
    
class RulesInput(BaseModel):
    character: RulesCharacter
    
class RulesOutput(BaseModel):
    character_name: str
    intent: str
    success: bool
    damage: int
    
class NPCOutput(BaseModel):
    character_name: str
    actions: str
    dialogue: str 
    
RulesInputSchema = RulesInput.schema()