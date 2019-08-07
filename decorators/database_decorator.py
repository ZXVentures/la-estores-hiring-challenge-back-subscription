import logging
from sqlalchemy.exc import IntegrityError

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

from la_estores_wrappers.utils.config import BaseConfig
from la_estores_wrappers.connectors import database_adapter

class Database(object):

    def __init__(self,secret_name):
        self.secret_name = secret_name

    def __call__(self, f):
        
        def run(**kwargs):
            
            secrets_adapter = AWSSecretsAdapter()
            database_configs = secrets_adapter.get_secret(secret_name)
            conn_string = database_adapter.get_conn_string(**database_configs)
            session = database_adapter.get_connection(conn_string)
            
            try:
        
                response = f(session=session, **kwargs)
                
                session.commit()
                
                return response
            
            except Exception as e:
                session.rollback()
                log.exception(str(e))
                raise
             
            finally:
                session.close()
            
        return run