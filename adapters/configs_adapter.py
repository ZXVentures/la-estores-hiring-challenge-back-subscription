import os, sys

import base64
import json

here = os.path.dirname(os.path.realpath(__file__))

class ConfigsAdapter():
    
    def __init__(self,scope=None):
        if not scope:
            scope = os.environ.get('scope','local')
        with open(f"{here}/../{scope}_config.json",'r') as file:
            contents = file.read()
            self.configs = json.loads(contents)

    def get_config(self,config_name):
        
        return self.configs.get(config_name)
        
        