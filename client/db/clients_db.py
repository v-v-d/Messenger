from contextlib import contextmanager
from datetime import datetime

from sqlalchemy import create_engine, MetaData, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from db.settings import DEFAULT_DB_CONNECTION_URL


ENGINE = create_engine(DEFAULT_DB_CONNECTION_URL, echo=False, pool_recycle=7200)
Base = declarative_base(metadata=MetaData(bind=ENGINE))
Session = sessionmaker(bind=ENGINE)


def migrate_db():
    """Propagate changes made to models into database schema."""
    Base.metadata.create_all(ENGINE)


@contextmanager
def session_scope(expire=True):
    """Database connection context manager."""
    if not isinstance(expire, bool):
        raise ValueError(f'Expire attr must be bool. Got {type(expire)}')

    session = Session()
    session.expire_on_commit = expire
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class Client(Base):
    """Client model."""
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    last_visit = Column(DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f'{self.name} {"is active" if self.is_active else "not active"}'
