# -*- coding: utf-8 -*-

import os, sys
import json

from adapters.configs_adapter import ConfigsAdapter

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

class Config(object):
    
    def __call__(self, f):
        
        def run(**kwargs):
            
            configs_adapter = ConfigsAdapter()
            
            f(configs_adapter=configs_adapter,**kwargs)
            
        return run

    