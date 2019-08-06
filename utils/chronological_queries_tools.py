
from utils.date_utility import DateUtility
from lib.data_access.db_model import Subscription,SubscriptionStatusHistory
from sqlalchemy import and_, desc, or_, extract, func

class ChronologicalQueriesTools():
    
    def __init__(
            self, 
            session
            ):
        self.session = session
        self.reference_date = DateUtility.utc_now()
    
    def group_subscriptions_per_current_status(self):
        csh_t = self.session.query(
            SubscriptionStatusHistory,
            func.row_number().\
            over(
                partition_by=SubscriptionStatusHistory.subscription_id,
                order_by=SubscriptionStatusHistory.effect_date.desc()).\
            label('row_number')
            ).\
            filter(
                SubscriptionStatusHistory.effect_date <= self.reference_date 
                ).\
            subquery('csh_t')
        csh = self.session.query(
            csh_t
            ).\
            filter(
                csh_t.c.row_number == 1
            ).\
            subquery('csh')
        
        return csh
        
        