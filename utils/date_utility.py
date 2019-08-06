import pytz
import time
from datetime import tzinfo, timedelta, datetime

class DateUtility():
    
    @classmethod
    def utc_min_tz(self):
        utc = pytz.timezone('utc')
        ref_date = datetime.min
        ref_date = utc.localize(ref_date)
        return ref_date
    
    @classmethod
    def utc_min(self):
        ref_date = datetime.min
        return ref_date
    
    @classmethod
    def utc_now_tz(self):
        ref_date = datetime.utcnow()
        utc = pytz.timezone('utc')
        ref_date = utc.localize(ref_date)
        return ref_date
    
    @classmethod
    def utc_now(self):
        ref_date = datetime.utcnow()
        return ref_date
    
    @classmethod
    def datetime(self, *args, **kwargs):
        return datetime(*args, **kwargs)
    
    @classmethod
    def now(self, *args, **kwargs):
        return datetime.now()