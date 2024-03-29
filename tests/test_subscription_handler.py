# -*- coding: utf-8 -*-
import json
import os
import sys

from tests.test_base import TestBase
from tests.mocks import boto3_mocker
from mock.mock import patch

from data_access.db_model import Status, SubscriptionStatusHistory
from utils.date_utility import DateUtility
from functions import subscription_handler as SubscriptionHandler
from datetime import datetime

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "."))
sys.path.append(os.path.join(here, ".."))

reference_date_iso = '2019-02-18T12:25:56.563000'
reference_date = datetime.strptime(reference_date_iso, "%Y-%m-%dT%H:%M:%S.%f")

class TestSubscriptionHandler(TestBase):

    @patch('utils.date_utility.DateUtility.utc_now', side_effect=lambda:reference_date)
    def test_update_status_pause(
        self
        ,boto_mock
        ):

        subscription_id = "00000000-0000-000-00000-000000000000"

        event = {
            'queryStringParameters': None,
            'pathParameters': {'id':f"{subscription_id}"},
            'body': f'''{{
                "status_id":{Status.PAUSED},
                "effect_date":"{reference_date_iso}",
                "interval":30
            }}'''
        }

        result = SubscriptionHandler.update_status(event,None)

        results = self.session.query(SubscriptionStatusHistory)\
            .filter(SubscriptionStatusHistory.subscription_id == subscription_id)\
            .order_by(SubscriptionStatusHistory.effect_date)\
            .all()
        
        assert results[0].status_id == Status.PAUSED
        assert results[1].status_id == Status.ACTIVE
        