import logging
from adapters import database_adapter

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

class Database(object):

    def __call__(self, f):
        
        def run(configs_adapter,**kwargs):
            
            database_configs = configs_adapter.get_config('database')
            conn_string = database_adapter.get_conn_string(**database_configs)
            session = database_adapter.get_connection(conn_string)
            
            try:
        
                response = f(session=session,configs_adapter=configs_adapter, **kwargs)
                
                session.commit()
                
                return response
            
            except Exception as e:
                session.rollback()
                log.exception(str(e))
                raise
             
            finally:
                session.close()
            
        return run