"""Server side database utilities for Messenger app."""
from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

from db.models import ENGINE, Base

Session = sessionmaker(bind=ENGINE)


def migrate_db():
    """Propagate changes made to models into database schema."""
    Base.metadata.create_all(ENGINE)


@contextmanager
def session_scope():
    """Database connection context manager."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
