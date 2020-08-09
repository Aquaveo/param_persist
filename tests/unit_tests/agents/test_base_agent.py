"""
Tests for the SqlAlchemy agent.

This file was created on August 06, 2020
"""
import pytest

from param_persist.agents.base import AgentBase


class BaseTestAgent(AgentBase):
    """A dummy agent class for testing."""
    def save(self, instance):
        """A dummy save function for testing the base class."""
        super().save(instance)

    def load(self, instance_id):
        """A dummy load function for testing the base class."""
        super().load(instance_id)

    def delete(self, instance_id):
        """A dummy delete function for testing the base class."""
        super().delete(instance_id)

    def update(self, instance, instance_id):
        """A dummy update function for testing the base class."""
        super().update(instance, instance_id)


def test_base_save():
    """Test the base save function raises a NotImplementedError."""
    base_test_agent = BaseTestAgent(None)

    with pytest.raises(NotImplementedError) as excinfo:
        base_test_agent.save(None)

    assert 'The "save" function must be overridden in the agent child class.' in str(excinfo.value)


def test_base_load():
    """Test the base load function raises a NotImplementedError."""
    base_test_agent = BaseTestAgent(None)

    with pytest.raises(NotImplementedError) as excinfo:
        base_test_agent.load(None)

    assert 'The "load" function must be overridden in the agent child class.' in str(excinfo.value)


def test_base_delete():
    """Test the base delete function raises a NotImplementedError."""
    base_test_agent = BaseTestAgent(None)

    with pytest.raises(NotImplementedError) as excinfo:
        base_test_agent.delete(None)

    assert 'The "delete" function must be overridden in the agent child class.' in str(excinfo.value)


def test_base_update():
    """Test the base update function raises a NotImplementedError."""
    base_test_agent = BaseTestAgent(None)

    with pytest.raises(NotImplementedError) as excinfo:
        base_test_agent.update(None, None)

    assert 'The "update" function must be overridden in the agent child class.' in str(excinfo.value)
