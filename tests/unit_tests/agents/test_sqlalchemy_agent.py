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

    print('-------' + '\n'.join(str(param_models)))
    assert param_model_count == 4


def test_load_param_using_sqlalchemy_engine():
    pass


def test_delete_param_using_sqlalchemy_engine():
    pass


def test_update_param_using_sqlalchemy_engine():
    pass
