"""
Abstract base class for agents.

This file was created on August 12, 2020
"""
from abc import ABC, abstractmethod
import importlib
import json

from param.serializer import JSONSerialization


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
    def save(self, instance, **kwargs):
        """
        An abstract function to save a persisted param class.
        """
        raise NotImplementedError('The "save" function must be overridden in the agent child class.')

    @abstractmethod
    def load(self, **kwargs):
        """
        An abstract function to load a persisted param class.
        """
        raise NotImplementedError('The "load" function must be overridden in the agent child class.')

    @abstractmethod
    def delete(self, **kwargs):
        """
        An abstract function to delete a persisted param class.
        """
        raise NotImplementedError('The "delete" function must be overridden in the agent child class.')

    @abstractmethod
    def update(self, instance, **kwargs):
        """
        An abstract function to update a persisted param class.
        """
        raise NotImplementedError('The "update" function must be overridden in the agent child class.')

    def get_serialized_param(self, instance):
        """
        Get the serialized parameter data.

        Args:
            instance: The instance to serialize

        Returns:
            Json serialization of the parameterized instance.
        """
        return json.loads(JSONSerialization.serialize_parameters(instance))

    @staticmethod
    def get_param_names(param_object):
        """
        Return list of all the names in param.
        """
        param_items = param_object.param.get_param_values()
        param_names = list()
        for item in param_items:
            param_names.append(item[0])

        return param_names

    @staticmethod
    def get_param_object_from_instance(instance_model):
        """
        Given an instance_model, return an associated param object.
        """
        # Getting param_object
        try:
            class_base_path, class_name = instance_model.class_path.rsplit('.', 1)
            param_module = importlib.import_module(class_base_path)
            parameterized_class = getattr(param_module, class_name)
        except ImportError:
            raise RuntimeError(f'Defined param class "class_path" was not importable.'
                               f' Given path is "{instance_model.class_path}"')

        param_object = parameterized_class()

        return param_object

    def update_param_object(self, param_object, serialized_data):
        """
        Update param_object data with given serialized data. Use JSONSerialization from param to deserialize the data.
        """
        # Update param object using deserialized data.
        param_names = self.get_param_names(param_object)

        # Remove extra args if needed.
        keys_to_remove = list()
        for key, _ in serialized_data.items():
            if key not in param_names:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            serialized_data.pop(key)

        # Deserialize param data
        param_model_deserialize = JSONSerialization. \
            deserialize_parameters(pobj=param_object, serialization=json.dumps(serialized_data))

        for key, value in param_model_deserialize.items():
            setattr(param_object, key, value)

        return param_object

    @staticmethod
    def load_serialized_data_from_param_model(param_models):
        """
        Load serialized data from param models in appropriated format.
        """
        param_models_json = [x.value for x in param_models]
        # Create serialized dictionary data in param serialized format to deserialize
        param_model_serialized_data = dict()

        for item in param_models_json:
            item = json.loads(item)
            param_model_serialized_data[item['name']] = item['value']

        return param_model_serialized_data

    @staticmethod
    def get_type_from_param_instance(instance, key):
        """
        Get the associated type from a key of an instance from the database.
        """
        type_string = '.'.join([type(instance.param.__getitem__(key)).__module__,
                                type(instance.param.__getitem__(key)).__name__]
                               )
        return type_string

    @staticmethod
    def get_class_path_from_param_instance(instance):
        """
        Get the associated class path of an instance from the database.
        """
        class_path = ".".join([
            instance.__module__,
            instance.__class__.__name__,
        ])
        return class_path
