# -*- coding: utf-8 -*-

import os, sys
import json

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "."))
sys.path.append(os.path.join(here, "../.."))

def _make_api_call(operation_name, *args, **kwargs):
    print('Boto mock')
    print(operation_name, args, kwargs)
    
    
        
        