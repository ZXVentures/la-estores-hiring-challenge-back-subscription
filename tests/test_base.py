# -*- coding: utf-8 -*-

import os, sys
from tests.mocks.data import base_data_mocks
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, '.'))
sys.path.append(os.path.join(here, '..'))

import json
from sqlalchemy.orm import RelationshipProperty, class_mapper
from sqlalchemy.orm.mapper import Mapper
from adapters import database_adapter
from data_access.db_model import build_model, drop_model, Subscription, Club
from adapters.configs_adapter import ConfigsAdapter

class TestBase(object):

    def _create_from_dict(self, d, clazz):
        map_relationship_class = {}
        f = filter(lambda x: isinstance(x, RelationshipProperty),
                   class_mapper(clazz).iterate_properties)
        for y in f:
            clazz_name = str(y).split('%s.' % clazz.__name__, 1)[1]
            if type(y.argument) != Mapper:
                map_relationship_class[clazz_name] = y.argument()

        attr = {}
        for k, v in d.items():
            if isinstance(v, dict):
                attr[k] = self._create_from_dict(v, map_relationship_class[k])
            elif isinstance(v, list):
                attr[k] = self._create_from_dict_list(v, map_relationship_class[k])
            else:
                attr[k] = v
        entity = clazz(**attr)
        self.session.add(entity)
        return entity

    def _create_from_dict_list(self, l, clazz):
        for x in l:
            self._create_from_dict(x, clazz)

    def _build_db(self, engine):
        build_model(engine)

    def _drop_db(self, engine):
        drop_model(engine)

    def _create_base_scenario(self):
        self._create_from_dict_list(base_data_mocks.CLUBS, Club)
        self._create_from_dict_list(base_data_mocks.SUBSCRIPTIONS, Subscription)

    def _create_specific_scenario(self):
        pass

    def _post_setup_amends(self, session):
        pass

    def setup(self):
        print('\nSetting Up!\n')

        configs_adapter = ConfigsAdapter('local')
        database_configs = configs_adapter.get_config('database')

        conn_string = database_adapter.get_conn_string(**database_configs)

        self.ENGINE = database_adapter.get_engine(conn_string)
        self._build_db(self.ENGINE)
        self.session = database_adapter.get_connection(conn_string)
        self._create_base_scenario()
        self._create_specific_scenario()
        self.session.commit()
        self._post_setup_amends(self.session)
        self.session.commit()

    def teardown(self):
        print('\nTearing down!\n')

        self.session.close()
        self._drop_db(self.ENGINE)
