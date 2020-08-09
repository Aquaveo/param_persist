"""
The conftest.py for the the agents test fixtures.

This file was created on August 06, 2020
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from param_persist.sqlalchemy.models import Base


@pytest.fixture(scope='session')
def sqlalchemy_engine():
    """
    Create engine.
    """
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture(scope='session')
def sqlalchemy_session_factory(sqlalchemy_engine):
    """
    Factory to create clean session for each test.
    """
    return scoped_session(sessionmaker(bind=sqlalchemy_engine))


@pytest.fixture(scope='session')
def sqlalchemy_session(sqlalchemy_session_factory):
    """
    Create session.
    """
    _session = sqlalchemy_session_factory()

    yield _session

    _session.rollback()
    _session.close()
