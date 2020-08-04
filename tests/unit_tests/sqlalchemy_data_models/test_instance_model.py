"""
Tests for the instance model in the sqlalchemy data model.

This file was generated on July 30, 2020
"""
from param_persist.sqlalchemy.models import InstanceModel, ParamModel


def test_delete_instance(db, session):
    """
    Test deleting an instance cascade deletes params.
    """
    instance_count = session.query(InstanceModel).count()
    instance = session.query(InstanceModel).first()
    instance_id = instance.id

    param_count = session.query(ParamModel).count()
    instance_param_count = session.query(ParamModel).filter_by(instance_id=instance_id).count()

    session.delete(instance)

    new_param_count = session.query(ParamModel).count()
    new_instance_count = session.query(InstanceModel).count()

    assert new_instance_count == instance_count - 1
    assert new_param_count == param_count - instance_param_count


def test_instance_repr(db, session):
    """
    Test the instance __repr__ function.
    """
    instance = session.query(InstanceModel).first()
    instance_repr = instance.__repr__()

    expected = f'<Instance(id="{instance.id}", class_path="{instance.class_path}")>'

    assert instance_repr == expected
