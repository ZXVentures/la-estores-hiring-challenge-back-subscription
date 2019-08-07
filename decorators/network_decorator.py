# -*- coding: utf-8 -*-

import os, sys
import json
from la_estores_wrappers.utils.config import BaseConfig, Tenant

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
            
            result = f(event=event,context=context,tenant=tenant)
            
            response['body'] = result
            response['statusCode'] = 200
            
        return run

    