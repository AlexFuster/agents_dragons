from common.agent import Agent
from common.models import SceneCharacter, SceneAddInput, SceneUpdateInput, SceneRemoveInput
import os
import json
from common.logging import config_logging

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SceneManager(Agent):
    def __init__(self):
        self.logger = config_logging("SceneManager")
        self.tools_exposed =[
            {
                "name": "add_character_to_scene",
                "description": """
                    Adds a character to the scene.
                    The orchestrator agent will call this method to add a new character to the scene.
                    Input: A character represented as a dictionary
                    Output: The updated scene with the new character added
                """,
                "input_model": SceneAddInput
            },
            {
                "name": "update_character_in_scene",
                "description": """
                    Updates an existing character in the scene.
                    The orchestrator agent will call this method to update an existing character in the scene.
                    Input: The name of the character to update, a list of keys to update and a list of new values for those keys
                    Output: The updated scene with the character updated
                """,
                "input_model": SceneUpdateInput
            },
            {
                "name": "remove_character_from_scene",
                "description": """
                    Removes a character from the scene.
                    The orchestrator agent will call this method to remove a character from the scene.
                    Input: The name of the character to remove
                    Output: The updated scene with the character removed
                """,
                "input_model": SceneRemoveInput
            }
        ]
        
        
        self.scene_path = os.path.join(root_dir, 'data', 'scene.json')
        if not os.path.exists(self.scene_path):
            with open(self.scene_path, 'w') as f:
                json.dump({"characters": []}, f)
                        
        with open(self.scene_path, 'r') as f:
            self.data = json.load(f)
            
    def get_scene(self):
        return self.data
    
    def add_character_to_scene(self, character: SceneCharacter):
        self.logger.info(f"Adding character to scene: {character}")
        self.data['characters'].append(character)
        with open(self.scene_path, 'w') as f:
            json.dump(self.data, f)
            
        self.logger.info(f"Current scene after adding character: {self.data}")
            
        return self.data
            
    def update_character_in_scene(self, name: str, keys_to_update: list, new_values: list):
        self.logger.info(f"Updating character in scene: {name}, keys to update: {keys_to_update}, new values: {new_values}")
        character = next((c for c in self.data['characters'] if c['name'] == name), None)
        if character:
            for key, value in zip(keys_to_update, new_values):
                character[key] = value
            with open(self.scene_path, 'w') as f:
                json.dump(self.data, f)
            return self.data
        else:
            raise ValueError(f"Character with name {name} not found in scene.")
        
    def remove_character_from_scene(self, name: str):
        self.logger.info(f"Removing character from scene: {name}")
        self.data['characters'] = [c for c in self.data['characters'] if c['name'] != name]
        with open(self.scene_path, 'w') as f:
            json.dump(self.data, f)
        return self.data