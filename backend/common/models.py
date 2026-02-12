from pydantic import BaseModel, Field
from typing import List, Literal


class OldCharacter(BaseModel):
    name: str
    type: str
    physical_description: str
    personality_description: str
    current_hp: int = Field(ge=0)
    distance_to_pj: Literal["none", "close", "near", "far"]
    is_pj: bool
    attitude: Literal["pos", "neg", "neutral"]
    


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