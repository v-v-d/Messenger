"""Server side database models for Messenger app."""
from sqlalchemy import (
    create_engine, MetaData,
    Column, Integer, String, DateTime, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from db.settings import DB_CONNECTION_URL

ENGINE = create_engine(DB_CONNECTION_URL, echo=False, pool_recycle=7200)
Base = declarative_base(metadata=MetaData(bind=ENGINE))


class Users(Base):
    """Users model."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False)
    password = Column(String(64), nullable=False)


class ActiveUsers(Base):
    """Active users model."""
    __tablename__ = 'active_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    addr = Column(String(64), nullable=False)
    port = Column(Integer, nullable=False)
    login_time = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', back_populates='active_users')


class LoginHistory(Base):
    """Login history model."""
    __tablename__ = 'login_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    addr = Column(String(64), nullable=False)
    port = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', back_populates='login_history')
