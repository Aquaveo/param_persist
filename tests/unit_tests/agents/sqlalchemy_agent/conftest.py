"""
The conftest.py for the the agents test fixtures.

This file was created on August 06, 2020
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, Session
import uuid

from param_persist.sqlalchemy.models import Base, InstanceModel, ParamModel


@pytest.fixture(scope='session')
def sqlalchemy_engine():
    """
    Create engine.
    """
    engine = create_engine('sqlite:///', echo=False)
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture(scope='session')
def sqlalchemy_session(sqlalchemy_engine):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = sqlalchemy_engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()


@pytest.fixture(scope='session')
def sqlalchemy_instance_model_complete(sqlalchemy_engine, sqlalchemy_session):
    """
    Create session-wide database.
    """
    # Instances
    instance_1 = InstanceModel(id=str(uuid.uuid4()),
                               class_path='tests.unit_tests.agents.sqlalchemy_agent.test_sqlalchemy_agent.TestParam')

    sqlalchemy_session.add(instance_1)

    # Params for Instance 1
    param_1_number = ParamModel(id=str(uuid.uuid4()),
                                value='{"name": "number_field", "type": "param.Number", "value": 1.7}',
                                instance_id=instance_1.id)
    param_1_integer = ParamModel(id=str(uuid.uuid4()),
                                 value='{"name": "integer_field", "type": "param.Number", "value": 9}',
                                 instance_id=instance_1.id)
    param_1_string = ParamModel(id=str(uuid.uuid4()),
                                value='{"name": "string_field", "type": "param.parameterized.String", '
                                      '"value": "Test String"}',
                                instance_id=instance_1.id)
    param_1_bool = ParamModel(id=str(uuid.uuid4()),
                              value='{"name": "boolean_field", "type": "param.Boolean", "value": true}',
                              instance_id=instance_1.id)

    sqlalchemy_session.add(param_1_number)
    sqlalchemy_session.add(param_1_integer)
    sqlalchemy_session.add(param_1_string)
    sqlalchemy_session.add(param_1_bool)

    sqlalchemy_session.commit()

    return instance_1


@pytest.fixture(scope='session')
def sqlalchemy_instance_model_missing(sqlalchemy_engine, sqlalchemy_session):
    """
    Create session-wide database.
    """
    # Instances
    instance_1 = InstanceModel(id=str(uuid.uuid4()),
                               class_path='tests.unit_tests.agents.sqlalchemy_agent.test_sqlalchemy_agent.TestParam')

    sqlalchemy_session.add(instance_1)

    # Params for Instance 1
    param_1_number = ParamModel(id=str(uuid.uuid4()),
                                value='{"name": "number_field", "type": "param.Number", "value": 1.7}',
                                instance_id=instance_1.id)
    param_1_bool = ParamModel(id=str(uuid.uuid4()),
                              value='{"name": "boolean_field", "type": "param.Boolean", "value": true}',
                              instance_id=instance_1.id)

    sqlalchemy_session.add(param_1_number)
    sqlalchemy_session.add(param_1_bool)

    sqlalchemy_session.commit()

    return instance_1


@pytest.fixture(scope='session')
def sqlalchemy_instance_model_extra(sqlalchemy_engine, sqlalchemy_session):
    """
    Create session-wide database.
    """
    # Instances
    instance_1 = InstanceModel(id=str(uuid.uuid4()),
                               class_path='tests.unit_tests.agents.sqlalchemy_agent.test_sqlalchemy_agent.TestParam')

    sqlalchemy_session.add(instance_1)

    # Params for Instance 1
    param_1_number = ParamModel(id=str(uuid.uuid4()),
                                value='{"name": "number_field", "type": "param.Number", "value": 1.7}',
                                instance_id=instance_1.id)
    param_1_integer = ParamModel(id=str(uuid.uuid4()),
                                 value='{"name": "integer_field", "type": "param.Number", "value": 9}',
                                 instance_id=instance_1.id)
    param_1_string = ParamModel(id=str(uuid.uuid4()),
                                value='{"name": "string_field", "type": "param.parameterized.String", '
                                      '"value": "Test String"}',
                                instance_id=instance_1.id)
    param_1_bool = ParamModel(id=str(uuid.uuid4()),
                              value='{"name": "boolean_field", "type": "param.Boolean", "value": true}',
                              instance_id=instance_1.id)
    param_1_garbage1 = ParamModel(id=str(uuid.uuid4()),
                                  value='{"name": "garbage_field_2", "type": "param.parameterized.String", '
                                        '"value": "Garbage TestString"}',
                                  instance_id=instance_1.id)
    param_1_garbage2 = ParamModel(id=str(uuid.uuid4()),
                                  value='{"name": "garbage_field_2", "type": "param.Boolean", "value": true}',
                                  instance_id=instance_1.id)

    sqlalchemy_session.add(param_1_number)
    sqlalchemy_session.add(param_1_integer)
    sqlalchemy_session.add(param_1_string)
    sqlalchemy_session.add(param_1_bool)
    sqlalchemy_session.add(param_1_garbage1)
    sqlalchemy_session.add(param_1_garbage2)

    sqlalchemy_session.commit()

    return instance_1

