"""Client side database models for Messenger app."""
from datetime import datetime

from sqlalchemy import (
    create_engine, MetaData, Column,
    Integer, String, DateTime, Boolean
)
from sqlalchemy.ext.declarative import declarative_base

from db.settings import DB_CONNECTION_URL

ENGINE = create_engine(
    DB_CONNECTION_URL, echo=False, pool_recycle=7200,
    connect_args={'check_same_thread': False}
)
Base = declarative_base(metadata=MetaData(bind=ENGINE))


class Message(Base):
    """Message model."""
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    edited = Column(Boolean, default=False)
    text = Column(String, nullable=False)
    created = Column(DateTime, nullable=False)
    from_client = Column(String, nullable=False)
    to_client = Column(String, nullable=False)

    def __repr__(self):
        return f'Client message'


class ClientSession(Base):
    """Client session model."""
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, nullable=False, unique=True)
    created = Column(DateTime, default=datetime.now())
    closed = Column(DateTime, nullable=True)
    remote_addr = Column(String, nullable=False)
    remote_port = Column(Integer, nullable=False)
    local_addr = Column(String, nullable=False)
    local_port = Column(Integer, nullable=False)

    def __repr__(self):
        return f'Client session'


class ClientContact(Base):
    """Client contact model."""
    __tablename__ = 'client_contacts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    confirmed = Column(Boolean, default=False)
    friend = Column(String, nullable=False)
    friend_id = Column(Integer, nullable=False)

    def __repr__(self):
        return f'Client contact list'
