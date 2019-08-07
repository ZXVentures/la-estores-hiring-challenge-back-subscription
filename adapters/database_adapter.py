
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


_CONNECTIONS = {}

def _bind_database(conn_string):
    
    if conn_string in _CONNECTIONS.keys():
        return
    
    engine = create_engine(conn_string)
            
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    
    _CONNECTIONS[conn_string]={}
    _CONNECTIONS[conn_string]['session'] = session
    _CONNECTIONS[conn_string]['engine'] = engine

def get_connection(conn_string):
    _bind_database(conn_string)
    return _CONNECTIONS[conn_string]['session']

def get_engine(conn_string):
    _bind_database(conn_string)
    return _CONNECTIONS[conn_string]['engine']

def get_conn_string(
        self,
        database_type,
        driver,
        db_user,
        db_password,
        db_host,
        db_port,
        db_name
    ):
    
    conn_string = f'{database_type}+{driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    return conn_string

    
    
