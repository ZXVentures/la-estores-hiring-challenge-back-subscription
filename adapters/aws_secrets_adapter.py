import os, sys

import boto3
import base64
import json

class AWSSecretsAdapter():
    
    def __init__(self):
        
        self.client = boto3.client(service_name='secretsmanager',region_name='us-west-2')
    
    def get_secret(self,screts_name):
        
        get_secret_value_response = self.client.get_secret_value(SecretId=screts_name)
        
        data = None
        
        if 'SecretString' in get_secret_value_response:
            data = get_secret_value_response['SecretString']
        else:
            data = base64.b64decode(get_secret_value_response['SecretBinary'])
            
        return json.loads(data)
        
        