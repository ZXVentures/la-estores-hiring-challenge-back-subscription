# -*- coding: utf-8 -*-

import os, sys
import json

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

class Network(object):
    
    def __call__(self, f):
        
        def run(event, context):
            log.info(event)
            
            response = {
                "headers":{
                    "content-type": "application/json"
                    },
                "statusCode": 500
            }
            
            event['body'] = json.loads(event['body'])
            
            result = f(event=event,context=context)
            
            response['body'] = result
            response['statusCode'] = 200
            
        return run

    