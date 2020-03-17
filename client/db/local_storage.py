"""Client side database utilities for Messenger app."""
from contextlib import contextmanager
from datetime import datetime

from sqlalchemy import (
    create_engine, MetaData, Column, Integer,
    Boolean, String, DateTime, Table, event
)
from sqlalchemy.orm import sessionmaker, mapper

from db.settings import BASE_DIR


class LocalStorage:
    def __init__(self, client_name):
        self.client_name = client_name
        self.engine = None
        self.metadata = None
        self.session = None

        self.set_session()

    def connect(self):
        self.set_engine()
        self.set_metadata()
        self.create_tables()
        self.set_session()

    def set_engine(self):
        db_connection_url = f'sqlite:///{BASE_DIR}/{self.client_name}.db'
        self.engine = create_engine(
            db_connection_url, echo=False, pool_recycle=7200,
            connect_args={'check_same_thread': False}
        )

    def set_metadata(self):
        self.metadata = MetaData()

    def set_session(self):
        self.session = sessionmaker(bind=self.engine)

    @contextmanager
    def session_scope(self, expire=True):
        """Database connection context manager."""
        if not isinstance(expire, bool):
            raise ValueError(f'Expire attr must be bool. Got {type(expire)}')

        session = self.session()
        session.expire_on_commit = expire
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    class Message:
        def __init__(self, text, created, from_client, to_client):
            self.id = None
            self.edited = None
            self.text = text
            self.created = created
            self.from_client = from_client
            self.to_client = to_client

        def __repr__(self):
            return 'Client message'

    class ClientSession:
        def __init__(self, token, remote_addr, remote_port, local_addr, local_port):
            self.id = None
            self.token = token
            self.created = None
            self.closed = None
            self.remote_addr = remote_addr
            self.remote_port = remote_port
            self.local_addr = local_addr
            self.local_port = local_port

        def __repr__(self):
            return 'Client session'

    class ClientContact:
        def __init__(self, friend, friend_id):
            self.id = None
            self.confirmed = None
            self.friend = friend
            self.friend_id = friend_id

        def __repr__(self):
            return f'Client contact'

    def create_tables(self):
        message = Table(
            'message', self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('edited', Boolean, default=False),
            Column('text', String, nullable=False),
            Column('created', DateTime, nullable=False),
            Column('from_client', String, nullable=False),
            Column('to_client', String, nullable=False),
        )
        client_session = Table(
            'client_session', self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('token', String, nullable=False, unique=True),
            Column('created', DateTime, default=datetime.now()),
            Column('closed', DateTime, nullable=True),
            Column('remote_addr', String, nullable=False),
            Column('remote_port', Integer, nullable=False),
            Column('local_addr', String, nullable=False),
            Column('local_port', Integer, nullable=False),
        )
        client_contact = Table(
            'client_contact', self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('confirmed', Boolean, default=False),
            Column('friend', String, nullable=False),
            Column('friend_id', Integer, nullable=False),
        )

        self.metadata.create_all(self.engine)

        mapper(self.Message, message)
        mapper(self.ClientSession, client_session)
        mapper(self.ClientContact, client_contact)


@event.listens_for(LocalStorage.ClientContact, 'after_insert')
@event.listens_for(LocalStorage.ClientContact, 'after_delete')
def on_contacts_changed(mapper, connection, target):
    from ui.signals import SIGNAL   # TODO: Вытащить импорт из триггера
    SIGNAL.contact_signal.emit()
