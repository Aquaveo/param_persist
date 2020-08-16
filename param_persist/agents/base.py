"""
Abstract base class for agents.

This file was created on August 12, 2020
"""
from abc import ABC, abstractmethod


class AgentBase(ABC):
    """
    The abstract base class for agents to inherit from.
    """

    def __init__(self, engine):
        """
        The __init__ for the agent base class.

        Args:
            engine: the engine to use for persisting.
        """
        self.engine = engine
        super().__init__()

    @abstractmethod
    def save(self, instance):
        """
        An abstract function to save a persisted param class.
        """
        raise NotImplementedError('The "save" function must be overridden in the agent child class.')

    @abstractmethod
    def load(self, instance_id):
        """
        An abstract function to load a persisted param class.
        """
        raise NotImplementedError('The "load" function must be overridden in the agent child class.')

    @abstractmethod
    def delete(self, instance_id):
        """
        An abstract function to delete a persisted param class.
        """
        raise NotImplementedError('The "delete" function must be overridden in the agent child class.')

    @abstractmethod
    def update(self, instance, instance_id):
        """
        An abstract function to update a persisted param class.
        """
        raise NotImplementedError('The "update" function must be overridden in the agent child class.')
