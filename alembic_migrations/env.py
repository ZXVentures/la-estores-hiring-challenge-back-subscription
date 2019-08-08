from __future__ import with_statement
import os
import sys
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, '.'))
sys.path.append(os.path.join(here, '..'))

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# this will overwrite the ini-file sqlalchemy.url path
# with the path given in the config of the main code
# ------------------------------------------------------
# command for generating new migration:
# alembic -x scope=test revision --autogenerate -m "Added feedback table"
# command for migrating db:
# alembic -x scope=test upgrade head
def get_local_connstring():
    import json
    from adapters import database_adapter
    arguments = context.get_x_argument(as_dictionary=True)
    scope = arguments.get('scope')
    if scope == 'build':
        secrets_adapter = AWSSecretsAdapter()
        database_configs = secrets_adapter.get_secret('la-estores-hiring-challenge-back-subscription-dbaccess')
        conn_string = database_adapter.get_conn_string(**database_configs)
    else:
        with open(f"{here}/../local/{scope}.json",'r') as file:
            contents = file.read()
            database_configs = json.loads(contents)

    conn_string = database_adapter.get_conn_string(**database_configs)
    return conn_string
#--------------------------------------------------------
config.set_main_option('sqlalchemy.url', get_local_connstring())

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from data_access import db_model
target_metadata = db_model.Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
#     raise Exception('Online migrations manually disabled due to connection config issues')
    run_migrations_online()
