
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
    
    def group_active_subscriptions_per_current_status(self):
        cssh_temp = self.session.query(
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
            subquery('cssh_temp')
        # cssh_cancelled = self.session.query(
        #     SubscriptionStatusHistory
        #     ).\
        #     filter(
        #         SubscriptionStatusHistory.status_id == Status.CANCELLED
        #     ).\
        #     subquery('cssh_cancelled')
        current_subscription_status_history = self.session.query(cssh_temp).\
            # join(cssh_cancelled, ssh.c.subscription_id != cssh_temp.c.subscription_id).\
            filter(
                cssh_temp.c.row_number == 1
            ).\
            subquery('current_subscription_status_history')
        
        
        
        
        return current_subscription_status_history
        
        