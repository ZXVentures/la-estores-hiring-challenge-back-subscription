# -*- coding: utf-8 -*-
import os, sys


from utils.date_utility import DateUtility
from utils.chronological_queries_tools import ChronologicalQueriesTools
from lib.data_access.db_model import Club, ClubStatus, ClubStatusHistory
from sqlalchemy import and_, desc, asc, func

class ClubRepository():
    
    def __init__(
            self, 
            session
            ):
        self.session = session
        self.reference_date = DateUtility.utc_now()
    
    def get_club_current_status_history_entry(
        self
        ,club_id
        ):
        result_status = self.session.\
            query(ClubStatusHistory).\
            filter(
                and_(
                    ClubStatusHistory.club_id == club_id,
                    ClubStatusHistory.effect_date <= self.reference_date
                    )
                ).\
            order_by(desc(ClubStatusHistory.effect_date)).\
            first()
              
        return result_status
