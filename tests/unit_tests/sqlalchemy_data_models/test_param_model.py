"""
Tests for the param model in the sqlalchemy data model.

This file was generated on July 31, 2020
"""
from param_persist.sqlalchemy.models import ParamModel


def test_param_repr(db, session):
    """
    Test the param __repr__ function.
    """
    param = session.query(ParamModel).first()
    param_repr = param.__repr__()

    expected = f'<Param(id="{param.id}", instance_id="{param.instance_id}")>'

    assert param_repr == expected
