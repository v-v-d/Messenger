"""Server side database models for Messenger app."""
from datetime import datetime

from sqlalchemy import (
    create_engine, MetaData, Column,
    Integer, String, DateTime, ForeignKey, Boolean
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from db.settings import DB_CONNECTION_URL

ENGINE = create_engine(DB_CONNECTION_URL, echo=False, pool_recycle=7200)
Base = declarative_base(metadata=MetaData(bind=ENGINE))


class Client(Base):
    """Client model."""
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    sent_messages = relationship('Message', foreign_keys='Message.from_client_id', back_populates='from_client')
    gotten_messages = relationship('Message', foreign_keys='Message.to_client_id', back_populates='to_client')
    sessions = relationship('ClientSession', back_populates='client')
    friends = relationship('ClientContact', foreign_keys='ClientContact.owner_id', back_populates='owner_contact')
    owners = relationship('ClientContact', foreign_keys='ClientContact.friend_id', back_populates='friend_contact')

    def __repr__(self):
        return self.name


class Message(Base):
    """Message model."""
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    created = Column(DateTime, nullable=False)
    from_client_id = Column(Integer, ForeignKey('clients.id'))
    to_client_id = Column(Integer, ForeignKey('clients.id'))
    from_client = relationship('Client', foreign_keys=[from_client_id], back_populates='sent_messages')
    to_client = relationship('Client', foreign_keys=[to_client_id], back_populates='gotten_messages')

    def __repr__(self):
        return self.text


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
    client_id = Column(Integer, ForeignKey('clients.id'))
    client = relationship('Client', back_populates='sessions')


class ClientContact(Base):
    """Client contact model."""
    __tablename__ = 'client_contacts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    confirmed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('clients.id'))
    friend_id = Column(Integer, ForeignKey('clients.id'))
    owner_contact = relationship('Client', foreign_keys=[owner_id], back_populates='friends')
    friend_contact = relationship('Client', foreign_keys=[friend_id], back_populates='owners')

    def __repr__(self):
        return f'{self.owner_contact} contact list'