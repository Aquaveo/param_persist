"""
Tests for the SqlAlchemy agent.

This file was created on August 06, 2020
"""
import json
import param

from param_persist.agents.sqlalchemy_agent import SqlAlchemyAgent
from param_persist.sqlalchemy.models import InstanceModel, ParamModel


class TestParam(param.Parameterized):
    """
    A Test param class for testing the serializer.
    """
    number_field = param.Number(0.5, doc="A simple number field.")
    integer_field = param.Integer(1, doc="A simple integer field.")
    string_field = param.String("My String", doc="A simple string field.")
    bool_field = param.Boolean(False, doc="A simple boolean field.")


def test_save_param_using_sqlalchemy_engine(sqlalchemy_engine, sqlalchemy_session):
    agent = SqlAlchemyAgent(sqlalchemy_engine)

    parameterized_class = TestParam()
    parameterized_class.number_field = 1.7
    parameterized_class.integer_field = 9
    parameterized_class.string_field = "Testing Strings"
    parameterized_class.bool_field = True

    returned_instance_model_id = agent.save(parameterized_class)

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


def test_load_param_using_sqlalchemy_engine(sqlalchemy_engine, sqlalchemy_session, sqlalchemy_instance_model_complete):
    agent = SqlAlchemyAgent(sqlalchemy_engine)

    instance_model = sqlalchemy_session.query(InstanceModel).filter_by(id=sqlalchemy_instance_model_complete.id)[0]
    assert instance_model.id == sqlalchemy_instance_model_complete.id

    parameterized_instance = agent.load(instance_model.id)

    assert type(parameterized_instance) is TestParam

    param_models = sqlalchemy_session.query(ParamModel).all()

    assert len(param_models) == 4
    for p in param_models:
        assert p.instance_id == instance_model.id
        param_dict = json.loads(p.value)
        assert getattr(parameterized_instance, param_dict['name']) == param_dict['value']
        parameter_type = type(getattr(parameterized_instance.param, param_dict['name']))
        base_type = '.'.join([parameter_type.__module__, parameter_type.__name__])
        assert base_type == param_dict['type']


def test_load_param_missing_param_fields(sqlalchemy_engine, sqlalchemy_session, sqlalchemy_instance_model_missing):
    agent = SqlAlchemyAgent(sqlalchemy_engine)

    instance_models = sqlalchemy_session.query(InstanceModel)
    assert instance_models.count() == 1
    instance_model = instance_models[0]
    assert instance_model.id == sqlalchemy_instance_model_missing.id

    parameterized_instance = agent.load(instance_model.id)

    assert type(parameterized_instance) is TestParam

    param_models = sqlalchemy_session.query(ParamModel).all()

    assert len(param_models) == 2
    for p in param_models:
        assert p.instance_id == instance_model.id
        param_dict = json.loads(p.value)
        assert getattr(parameterized_instance, param_dict['name']) == param_dict['value']
        parameter_type = type(getattr(parameterized_instance.param, param_dict['name']))
        base_type = '.'.join([parameter_type.__module__, parameter_type.__name__])
        assert base_type == param_dict['type']

    assert parameterized_instance.integer_field == 1
    assert parameterized_instance.string_field == "My String"


def test_load_param_extra_param_fields(sqlalchemy_engine, sqlalchemy_session, sqlalchemy_instance_model_extra):
    agent = SqlAlchemyAgent(sqlalchemy_engine)

    instance_model = sqlalchemy_session.query(InstanceModel).first()
    assert instance_model.id == sqlalchemy_instance_model_extra.id

    parameterized_instance = agent.load(instance_model.id)

    assert type(parameterized_instance) is TestParam

    param_models = sqlalchemy_session.query(ParamModel).all()

    assert len(param_models) == 6
    for p in param_models:
        assert p.instance_id == instance_model.id
        param_dict = json.loads(p.value)
        param_value = getattr(parameterized_instance, param_dict['name'], None)
        if param_value is None:
            assert param_dict['name'] in ['garbage_field_1', 'garbage_field_2']
        assert param_value == param_dict['value']
        parameter_type = type(getattr(parameterized_instance.param, param_dict['name']))
        base_type = '.'.join([parameter_type.__module__, parameter_type.__name__])
        assert base_type == param_dict['type']

    assert parameterized_instance.integer_field == 1
    assert parameterized_instance.string_field == "My String"


def test_delete_param_using_sqlalchemy_engine():
    pass


def test_update_param_using_sqlalchemy_engine():
    pass
