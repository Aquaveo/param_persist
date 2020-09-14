"""
Tests for the SqlAlchemy agent.

This file was created on August 06, 2020
"""
import json
import logging

import param
import pytest

from param_persist.agents.sqlalchemy_agent import SqlAlchemyAgent
from param_persist.sqlalchemy.models import InstanceModel, ParamModel


class AgentTestParam(param.Parameterized):
    """
    A Test param class for testing the serializer.
    """
    number_field = param.Number(0.5, doc="A simple number field.")
    integer_field = param.Integer(1, doc="A simple integer field.")
    string_field = param.String("My String", doc="A simple string field.")
    bool_field = param.Boolean(False, doc="A simple boolean field.")


class AgentTestParamMissing(param.Parameterized):
    """
    A Test param class for testing the serializer.
    """
    integer_field = param.Integer(1, doc="A simple integer field.")
    string_field = param.String("My String", doc="A simple string field.")
    bool_field = param.Boolean(False, doc="A simple boolean field.")


def test_save_param_using_sqlalchemy_engine(sqlalchemy_engine, sqlalchemy_session_factory):
    """
    Test the save function of the param persist sqlalchemy agent.
    """
    agent = SqlAlchemyAgent(sqlalchemy_engine)

    parameterized_class = AgentTestParam()
    parameterized_class.number_field = 1.7
    parameterized_class.integer_field = 9
    parameterized_class.string_field = "Testing Strings"
    parameterized_class.bool_field = True

    returned_instance_model_id = agent.save(parameterized_class)

    sqlalchemy_session = sqlalchemy_session_factory()
    instance_model_count = sqlalchemy_session.query(InstanceModel).count()
    instance_model_id = sqlalchemy_session.query(InstanceModel).first().id

    assert instance_model_count == 1
    assert returned_instance_model_id == instance_model_id

    param_model_count = sqlalchemy_session.query(ParamModel).count()
    param_models = sqlalchemy_session.query(ParamModel).all()

    for p in param_models:
        assert p.instance_id == instance_model_id
        param_dict = json.loads(p.value)
        assert getattr(parameterized_class, param_dict['name']) == param_dict['value']
        parameter_type = type(getattr(parameterized_class.param, param_dict['name']))
        base_type = '.'.join([parameter_type.__module__, parameter_type.__name__])
        assert base_type == param_dict['type']

    assert param_model_count == 4


def test_load_param_using_sqlalchemy_engine(sqlalchemy_engine, sqlalchemy_session_factory,
                                            sqlalchemy_instance_model_complete):
    """
    Test the load function of the param persist sqlalchemy agent with an invalid class.
    """
    agent = SqlAlchemyAgent(sqlalchemy_engine)

    sqlalchemy_session = sqlalchemy_session_factory()
    instance_model = sqlalchemy_session.query(InstanceModel).filter_by(id=sqlalchemy_instance_model_complete.id).first()
    assert instance_model.id == sqlalchemy_instance_model_complete.id
    param_models = [x for x in sqlalchemy_session.query(ParamModel).filter_by(instance_id=instance_model.id)]
    assert len(param_models) == 4

    parameterized_instance = agent.load(instance_model.id)

    assert type(parameterized_instance) is AgentTestParam

    for p in param_models:
        assert p.instance_id == instance_model.id
        param_dict = json.loads(p.value)
        assert getattr(parameterized_instance, param_dict['name']) == param_dict['value']
        parameter_type = type(getattr(parameterized_instance.param, param_dict['name']))
        base_type = '.'.join([parameter_type.__module__, parameter_type.__name__])
        assert base_type == param_dict['type']


def test_load_param_missing_param_fields(sqlalchemy_engine, sqlalchemy_session_factory,
                                         sqlalchemy_instance_model_missing):
    """
    Test the load function of the param persist sqlalchemy agent with an missing fields.
    """
    agent = SqlAlchemyAgent(sqlalchemy_engine)

    sqlalchemy_session = sqlalchemy_session_factory()
    instance_model = sqlalchemy_session.query(InstanceModel).filter_by(id=sqlalchemy_instance_model_missing.id).first()
    assert instance_model.id == sqlalchemy_instance_model_missing.id
    param_models = [x for x in sqlalchemy_session.query(ParamModel).filter_by(instance_id=instance_model.id)]
    assert len(param_models) == 2

    parameterized_instance = agent.load(instance_model.id)

    assert type(parameterized_instance) is AgentTestParam

    for p in param_models:
        assert p.instance_id == instance_model.id
        param_dict = json.loads(p.value)
        assert getattr(parameterized_instance, param_dict['name']) == param_dict['value']
        parameter_type = type(getattr(parameterized_instance.param, param_dict['name']))
        base_type = '.'.join([parameter_type.__module__, parameter_type.__name__])
        assert base_type == param_dict['type']

    assert parameterized_instance.integer_field == 1
    assert parameterized_instance.string_field == "My String"


def test_load_param_extra_param_fields(sqlalchemy_engine, sqlalchemy_session_factory,
                                       sqlalchemy_instance_model_extra):
    """
    Test the load function of the param persist sqlalchemy agent with extra fields.
    """
    agent = SqlAlchemyAgent(sqlalchemy_engine)

    sqlalchemy_session = sqlalchemy_session_factory()
    instance_model = sqlalchemy_session.query(InstanceModel).filter_by(id=sqlalchemy_instance_model_extra.id).first()
    assert instance_model.id == sqlalchemy_instance_model_extra.id

    param_models = [x for x in sqlalchemy_session.query(ParamModel).filter_by(instance_id=instance_model.id)]
    assert len(param_models) == 6

    parameterized_instance = agent.load(instance_model.id)

    assert type(parameterized_instance) is AgentTestParam
    assert len(param_models) == 6
    for p in param_models:
        assert p.instance_id == instance_model.id
        param_dict = json.loads(p.value)
        param_value = getattr(parameterized_instance, param_dict['name'], None)
        if param_value is None:
            assert param_dict['name'] in ['garbage_field_1', 'garbage_field_2']
            continue
        assert param_value == param_dict['value']
        parameter_type = type(getattr(parameterized_instance.param, param_dict['name']))
        base_type = '.'.join([parameter_type.__module__, parameter_type.__name__])
        assert base_type == param_dict['type']


def test_load_param_with_invalid_class(sqlalchemy_engine, sqlalchemy_instance_invalid_class):
    """
    Test the load function of the param persist sqlalchemy agent with an invalid class.
    """
    agent = SqlAlchemyAgent(sqlalchemy_engine)

    with pytest.raises(Exception) as excinfo:
        agent.load(sqlalchemy_instance_invalid_class.id)

    assert 'Defined param class "class_path" was not importable. ' \
           'Given path is "this.is.not.a.valid.module.InvalidParamClass"' in str(excinfo.value)


def test_delete_param_using_sqlalchemy_engine(sqlalchemy_engine, sqlalchemy_session_factory,
                                              sqlalchemy_instance_model_complete):
    """
    Test the delete function of the param persist sqlalchemy agent.
    """
    agent = SqlAlchemyAgent(sqlalchemy_engine)
    sqlalchemy_session = sqlalchemy_session_factory()
    assert 1 == sqlalchemy_session.query(InstanceModel).count()

    instance_model = sqlalchemy_session.query(InstanceModel).filter_by(id=sqlalchemy_instance_model_complete.id).first()
    agent.delete(instance_model.id)

    assert 0 == sqlalchemy_session.query(InstanceModel).count()


def test_delete_param_exception(sqlalchemy_engine, caplog):
    """
    Test the delete function of the param persist sqlalchemy agent using a bad id.
    """
    agent = SqlAlchemyAgent(sqlalchemy_engine)
    with caplog.at_level(logging.WARNING):
        agent.delete('not-a-valid-uuid')
    assert 'unable to query database with given instance id. id="not-a-valid-uuid"' in str(caplog.text)


def test_update_param_using_sqlalchemy_engine(sqlalchemy_engine, sqlalchemy_session_factory,
                                              sqlalchemy_instance_model_complete):
    """
    Test the update function of the param persist sqlalchemy agent.
    """
    agent = SqlAlchemyAgent(sqlalchemy_engine)

    parameterized_class = AgentTestParam()
    parameterized_class.number_field = 3.21
    parameterized_class.integer_field = 123
    parameterized_class.string_field = "Updated Strings"
    parameterized_class.bool_field = False

    returned_instance_model_id = agent.update(parameterized_class, sqlalchemy_instance_model_complete.id)

    sqlalchemy_session = sqlalchemy_session_factory()
    instance_model_count = sqlalchemy_session.query(InstanceModel).count()
    instance_model_id = sqlalchemy_session.query(InstanceModel).first().id

    assert instance_model_count == 1
    assert returned_instance_model_id == instance_model_id

    param_model_count = sqlalchemy_session.query(ParamModel).count()
    param_models = sqlalchemy_session.query(ParamModel).all()

    for p in param_models:
        assert p.instance_id == instance_model_id
        param_dict = json.loads(p.value)
        assert getattr(parameterized_class, param_dict['name']) == param_dict['value']
        parameter_type = type(getattr(parameterized_class.param, param_dict['name']))
        base_type = '.'.join([parameter_type.__module__, parameter_type.__name__])
        assert base_type == param_dict['type']

    assert param_model_count == 4


def test_update_param_bad_instance_id(sqlalchemy_engine):
    """
    Test the update function of the param persist sqlalchemy agent with a bad id.
    """
    agent = SqlAlchemyAgent(sqlalchemy_engine)
    parameterized_class = AgentTestParam()
    with pytest.raises(Exception) as excinfo:
        agent.update(parameterized_class, 'not-a-valid-uuid')

    assert 'Parameterized instance with id "not-a-valid-uuid" does not exist.' in str(excinfo.value)


def test_update_param_removing_attribute(sqlalchemy_engine, sqlalchemy_session_factory,
                                         sqlalchemy_instance_model_complete):
    """
    Test what happens when you update a instance model and params after removing a field.
    """
    agent = SqlAlchemyAgent(sqlalchemy_engine)

    parameterized_class = AgentTestParamMissing()

    parameterized_class.integer_field = 123
    parameterized_class.string_field = "Updated Strings"
    parameterized_class.bool_field = False

    returned_instance_model_id = agent.update(parameterized_class, sqlalchemy_instance_model_complete.id)

    sqlalchemy_session = sqlalchemy_session_factory()
    instance_model_count = sqlalchemy_session.query(InstanceModel).count()
    instance_model_id = sqlalchemy_session.query(InstanceModel).first().id

    assert instance_model_count == 1
    assert returned_instance_model_id == instance_model_id

    param_model_count = sqlalchemy_session.query(ParamModel).count()
    param_models = sqlalchemy_session.query(ParamModel).all()

    for p in param_models:
        assert p.instance_id == instance_model_id
        param_dict = json.loads(p.value)
        assert getattr(parameterized_class, param_dict['name']) == param_dict['value']
        parameter_type = type(getattr(parameterized_class.param, param_dict['name']))
        base_type = '.'.join([parameter_type.__module__, parameter_type.__name__])
        assert base_type == param_dict['type']

    assert param_model_count == 3
