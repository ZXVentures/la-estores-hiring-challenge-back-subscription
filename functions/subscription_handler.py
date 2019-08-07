
from data_access.db_model import Status
from repositories.subscription_repository import SubscriptionRepository
from datetime import datetime,timedelta

@Network()
@Database()
def update_status(session,event,context):

    body = event['body']
    subscription_id = body['subscription_id']
    status_id = body['status_id']
    effect_date = datetime.strptime(body['effect_date'], "%Y-%m-%dT%H:%M:%S.%fZ")
    details = body.get('details')
    interval = int(body['interval'])

    subscription_repository = SubscriptionRepository(session)
    subscription_repository.insert_status(
        subscription_id,
        status_id,
        effect_date,
        details
    )

    if status_id == Status.PAUSED:
        subscription_repository = SubscriptionRepository(session)
        return_date = effect_date.timedelta(interval)
        subscription_repository.insert_status(
            subscription_id,
            status_id,
            return_date,
            'Automatic return schedule'
        )