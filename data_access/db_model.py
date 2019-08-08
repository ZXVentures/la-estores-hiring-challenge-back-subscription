import uuid, sys, os

from utils.date_utility import DateUtility
from sqlalchemy import Column, ForeignKey, String, Integer, Text, Float, DateTime, Boolean, Binary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.sqltypes import Numeric
from sqlalchemy.orm.persistence import post_update
from sqlalchemy.sql.schema import ForeignKeyConstraint

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class ClubStatus(Base):
    __tablename__ = 'club_status'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    name = Column(String(128))
    create_date = Column(DateTime, default=DateUtility.utc_now)
    
    club_status_history = relationship("ClubStatusHistory", back_populates="club_status")

    ACTIVE = 1
    CLOSED = 2
    INACTIVE = 3
    
class ClubStatusHistory(Base):
    __tablename__ = 'club_status_history'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    
    club_id = Column(Integer, ForeignKey('club.id', ondelete="RESTRICT"))
    club_status_id = Column(Integer, ForeignKey('club_status.id', ondelete="RESTRICT"))
    effect_date = Column(DateTime, default=DateUtility.utc_now())
    create_date = Column(DateTime, default=DateUtility.utc_now())
    details = Column(String(256))
    
    club = relationship("Club",back_populates="club_status_history")
    club_status = relationship("ClubStatus",back_populates="club_status_history")


class Club(Base):
    __tablename__ = 'club'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    name = Column(String(128))
    store_sku = Column(Integer)
    
    club_status_history = relationship("ClubStatusHistory", back_populates="club")
    subscription_list = relationship("Subscription", back_populates="club")
    
    
class Subscription(Base):
    __tablename__ = 'subscription'
    
    id = Column("id",String(36), primary_key=True, default=generate_uuid)
    
    club_id = Column(Integer, ForeignKey('club.id', ondelete="RESTRICT"))
    customer_store_id = Column(String(36))
    create_date = Column(DateTime, default=DateUtility.utc_now)
    
    club = relationship("Club",back_populates="subscription_list",uselist=False)
    subscription_status_history = relationship("SubscriptionStatusHistory",back_populates="subscription")

class Status(Base):
    __tablename__ = 'status'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    name = Column(String(128))
    create_date = Column(DateTime, default=DateUtility.utc_now())
    
    subscription_status_history = relationship("SubscriptionStatusHistory", back_populates="status")
    
    ACTIVE = 1
    CANCELLED = 2
    PAUSED = 3
    
class SubscriptionStatusHistory(Base):
    __tablename__ = 'subscription_status_history'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    
    subscription_id = Column(String(36), ForeignKey('subscription.id', ondelete="RESTRICT"))
    status_id = Column(Integer, ForeignKey('status.id', ondelete="RESTRICT"))
    effect_date = Column(DateTime, default=DateUtility.utc_now())
    create_date = Column(DateTime, default=DateUtility.utc_now())
    details = Column(String(256))
    
    subscription = relationship("Subscription",back_populates="subscription_status_history")
    status = relationship("Status",back_populates="subscription_status_history")


here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, '.'))
sys.path.append(os.path.join(here, '..'))

def build_model(engine):
    drop_model(engine)
    import alembic.config
    alembicArgs = [
        '-x', 'scope=local',
        'upgrade', 'head', 
    ]
    alembic.config.main(argv=alembicArgs)

def drop_model(engine):
    import alembic.config
    alembicArgs = [
        '-x', 'scope=local',
        'downgrade', 'base',
    ]
    alembic.config.main(argv=alembicArgs)
    
    Base.metadata.drop_all(bind=engine)
    
