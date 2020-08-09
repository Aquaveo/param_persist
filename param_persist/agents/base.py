from abc import ABC, abstractmethod


class AgentBase(ABC):
    def __init__(self, engine):
        self.engine = engine
        super().__init__()

    @abstractmethod
    def save(self, instance):
        pass

    @abstractmethod
    def load(self, instance_id):
        pass

    @abstractmethod
    def delete(self, instance_id):
        pass

    @abstractmethod
    def update(self, instance, instance_id):
        pass
