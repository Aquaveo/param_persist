"""
The conftest.py for the the agents test fixtures.

This file was created on August 06, 2020
"""
import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from param_persist.sqlalchemy.models import Base, InstanceModel, ParamModel


@pytest.yield_fixture(scope='function')
def sqlalchemy_engine():
    """
    Create engine.
    """
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.yield_fixture(scope='function')
def sqlalchemy_session_factory(sqlalchemy_engine):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    sessions = []
    transactions = []
    connections = []

    def _sqlalchemy_session_factory():
        connection = sqlalchemy_engine.connect()
        connections.append(connection)
        # begin the nested transaction
        transaction = connection.begin()
        transactions.append(transaction)
        # use the connection with the already started transaction
        session = Session(bind=connection)
        sessions.append(session)

        return session

    yield _sqlalchemy_session_factory

    for session in sessions:
        session.close()
    for transaction in transactions:
        transaction.rollback()
    for connection in connections:
        connection.close()


@pytest.fixture()
def sqlalchemy_instance_model_complete(sqlalchemy_session_factory):
    """
    Create session-wide database.
    """
    sqlalchemy_session = sqlalchemy_session_factory()

    # Instances
    instance_1 = InstanceModel(id=str(uuid.uuid4()),
                               class_path='tests.unit_tests.agents.sqlalchemy_agent.'
                                          'test_sqlalchemy_agent.AgentTestParam')

    sqlalchemy_session.add(instance_1)

    # Params for Instance 1
    param_1_number = ParamModel(id=str(uuid.uuid4()),
                                value='{"name": "number_field", "type": "param.Number", "value": 1.7}',
                                instance_id=instance_1.id)
    param_1_integer = ParamModel(id=str(uuid.uuid4()),
                                 value='{"name": "integer_field", "type": "param.Integer", "value": 9}',
                                 instance_id=instance_1.id)
    param_1_string = ParamModel(id=str(uuid.uuid4()),
                                value='{"name": "string_field", "type": "param.parameterized.String", '
                                      '"value": "Test String"}',
                                instance_id=instance_1.id)
    param_1_bool = ParamModel(id=str(uuid.uuid4()),
                              value='{"name": "bool_field", "type": "param.Boolean", "value": true}',
                              instance_id=instance_1.id)

    sqlalchemy_session.add(param_1_number)
    sqlalchemy_session.add(param_1_integer)
    sqlalchemy_session.add(param_1_string)
    sqlalchemy_session.add(param_1_bool)

    sqlalchemy_session.commit()

    return instance_1


@pytest.fixture()
def sqlalchemy_instance_model_missing(sqlalchemy_session_factory):
    """
    Create session-wide database.
    """
    sqlalchemy_session = sqlalchemy_session_factory()

    # Instances
    instance_1 = InstanceModel(id=str(uuid.uuid4()),
                               class_path='tests.unit_tests.agents.sqlalchemy_agent.'
                                          'test_sqlalchemy_agent.AgentTestParam')

    sqlalchemy_session.add(instance_1)

    # Params for Instance 1
    param_1_number = ParamModel(id=str(uuid.uuid4()),
                                value='{"name": "number_field", "type": "param.Number", "value": 1.7}',
                                instance_id=instance_1.id)
    param_1_bool = ParamModel(id=str(uuid.uuid4()),
                              value='{"name": "bool_field", "type": "param.Boolean", "value": true}',
                              instance_id=instance_1.id)

    sqlalchemy_session.add(param_1_number)
    sqlalchemy_session.add(param_1_bool)

    sqlalchemy_session.commit()

    return instance_1


@pytest.fixture()
def sqlalchemy_instance_model_extra(sqlalchemy_session_factory):
    """
    Create session-wide database.
    """
    sqlalchemy_session = sqlalchemy_session_factory()

    # Instances
    instance_1 = InstanceModel(id=str(uuid.uuid4()),
                               class_path='tests.unit_tests.agents.sqlalchemy_agent.'
                                          'test_sqlalchemy_agent.AgentTestParam')

    sqlalchemy_session.add(instance_1)

    # Params for Instance 1
    param_1_number = ParamModel(id=str(uuid.uuid4()),
                                value='{"name": "number_field", "type": "param.Number", "value": 1.7}',
                                instance_id=instance_1.id)
    param_1_integer = ParamModel(id=str(uuid.uuid4()),
                                 value='{"name": "integer_field", "type": "param.Integer", "value": 9}',
                                 instance_id=instance_1.id)
    param_1_string = ParamModel(id=str(uuid.uuid4()),
                                value='{"name": "string_field", "type": "param.parameterized.String", '
                                      '"value": "Test String"}',
                                instance_id=instance_1.id)
    param_1_bool = ParamModel(id=str(uuid.uuid4()),
                              value='{"name": "bool_field", "type": "param.Boolean", "value": true}',
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


@pytest.fixture()
def sqlalchemy_instance_invalid_class(sqlalchemy_session_factory):
    """
    Create session-wide database.
    """
    sqlalchemy_session = sqlalchemy_session_factory()

    # Instances
    instance_1 = InstanceModel(id=str(uuid.uuid4()),
                               class_path='this.is.not.a.valid.module.InvalidParamClass')

    sqlalchemy_session.add(instance_1)

    # Params for Instance 1
    param_1_number = ParamModel(id=str(uuid.uuid4()),
                                value='{"name": "number_field", "type": "param.Number", "value": 1.7}',
                                instance_id=instance_1.id)
    param_1_integer = ParamModel(id=str(uuid.uuid4()),
                                 value='{"name": "integer_field", "type": "param.Integer", "value": 9}',
                                 instance_id=instance_1.id)
    param_1_string = ParamModel(id=str(uuid.uuid4()),
                                value='{"name": "string_field", "type": "param.parameterized.String", '
                                      '"value": "Test String"}',
                                instance_id=instance_1.id)
    param_1_bool = ParamModel(id=str(uuid.uuid4()),
                              value='{"name": "bool_field", "type": "param.Boolean", "value": true}',
                              instance_id=instance_1.id)

    sqlalchemy_session.add(param_1_number)
    sqlalchemy_session.add(param_1_integer)
    sqlalchemy_session.add(param_1_string)
    sqlalchemy_session.add(param_1_bool)

    sqlalchemy_session.commit()

    return instance_1
