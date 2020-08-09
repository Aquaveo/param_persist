from abc import ABC, abstractmethod


class AgentBase(ABC):
    def __init__(self, engine):
        self.engine = engine
        super().__init__()

    @abstractmethod
    def save(self, instance):
        raise NotImplementedError('The "save" function must be overridden in the agent child class.')

    @abstractmethod
    def load(self, instance_id):
        raise NotImplementedError('The "load" function must be overridden in the agent child class.')

    @abstractmethod
    def delete(self, instance_id):
        raise NotImplementedError('The "delete" function must be overridden in the agent child class.')

    @abstractmethod
    def update(self, instance, instance_id):
        raise NotImplementedError('The "update" function must be overridden in the agent child class.')
