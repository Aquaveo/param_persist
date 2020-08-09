"""
PyTest configuration for the sqlalchemy data models tests.

This file was generated on July 30, 2020
"""
import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from param_persist.sqlalchemy.models import Base, InstanceModel, ParamModel


@pytest.fixture(scope='session')
def engine():
    """
    Create engine.
    """
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture(scope='session')
def session_factory(engine):
    """
    Factory to create clean session for each test.
    """
    return scoped_session(sessionmaker(bind=engine))


@pytest.fixture(scope='session')
def session(session_factory):
    """
    Create session.
    """
    _session = session_factory()

    yield _session

    _session.rollback()
    _session.close()


@pytest.fixture(scope='session')
def db(engine, session):
    """
    Create session-wide database.
    """
    # Instances
    instance_1 = InstanceModel(id=str(uuid.uuid4()), class_path='paramclass.param.ParamClass1')
    instance_2 = InstanceModel(id=str(uuid.uuid4()), class_path='paramclass.param.ParamClass1')
    instance_3 = InstanceModel(id=str(uuid.uuid4()), class_path='paramclass.param.ParamClass2')

    session.add(instance_1)
    session.add(instance_2)
    session.add(instance_3)

    # Params for Instance 1
    param_1 = ParamModel(id=str(uuid.uuid4()), value='{"name": "param1_1", "type": "string", "value": "string_value1"}',
                         instance_id=instance_1.id)

    # Params for Instance 2
    param_2 = ParamModel(id=str(uuid.uuid4()), value='{"name": "param2_1", "type": "string", "value": "string_value1"}',
                         instance_id=instance_2.id)
    param_3 = ParamModel(id=str(uuid.uuid4()), value='{"name": "param2_2", "type": "string", "value": "1234"}',
                         instance_id=instance_2.id)

    # Params for Instance 2
    param_4 = ParamModel(id=str(uuid.uuid4()), value='{"name": "param3_1", "type": "int", "value": 12}',
                         instance_id=instance_3.id)
    param_5 = ParamModel(id=str(uuid.uuid4()), value='{"name": "param3_2", "type": "string", "value": "1234"}',
                         instance_id=instance_3.id)
    param_6 = ParamModel(id=str(uuid.uuid4()), value='{"name": "param3_3", "type": "float", "value": 123.321}',
                         instance_id=instance_3.id)

    session.add(param_1)
    session.add(param_2)
    session.add(param_3)
    session.add(param_4)
    session.add(param_5)
    session.add(param_6)

    session.commit()

    return Base
