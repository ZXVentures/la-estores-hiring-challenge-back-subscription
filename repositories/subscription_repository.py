# -*- coding: utf-8 -*-

from data_access.db_model import SubscriptionStatusHistory

class SubscriptionRepository():

    def __init__(self, session):
        self.session = session
        
    def insert_status(
        self,
        subscription_id,
        status_id,
        effect_date,
        details = None
        ):

        subscription_status_history_entry = SubscriptionStatusHistory()
        subscription_status_history_entry.subscription_id = subscription_id
        subscription_status_history_entry.status_id = status_id
        subscription_status_history_entry.effect_date = effect_date
        subscription_status_history_entry.details = details

        self.session.add(subscription_status_history_entry)

        return subscription_status_history_entry