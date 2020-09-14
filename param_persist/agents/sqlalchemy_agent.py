"""
The SqlAlchemy Agent.

This file was created on August 05, 2020
"""

import importlib
import json
import logging
import uuid

from param.serializer import JSONSerialization
from sqlalchemy.orm import sessionmaker

from param_persist.agents.base import AgentBase
from param_persist.sqlalchemy.models import InstanceModel, ParamModel

log = logging.getLogger('param_persist')


def sqlalchemy_session(wrapped_function):
    """
    Decorator for creating, closeing and rolling back an sqlalchemy session.
    """
    def decorator_function(self, *args, **kwargs):
        db_session = self.make_session()

        try:
            return wrapped_function(self, *args, db_session=db_session, **kwargs)
        except Exception:
            db_session.rollback()
            raise
        finally:
            db_session.close()

    return decorator_function


class SqlAlchemyAgent(AgentBase):
    """
    An agent for persisting parameterized objects to SQL databases.
    """

    def __init__(self, engine):
        """
        The __init__ function for the the SqlAlchemyAgent.
        """
        super().__init__(engine)
        self.make_session = sessionmaker(bind=self.engine)

    @sqlalchemy_session
    def save(self, instance, **kwargs):
        """
        Save a parameterized instance to a sqlalchemy database.

        Args:
            instance: The parameterized instance to be saved to the database.

        Returns:
            The id of the row in the database corresponding to the parameterized instance.
        """
        db_session = kwargs.get('db_session', None)

        # Serialize data using param JSONSerialization class
        serialized_param = json.loads(JSONSerialization.serialize_parameters(instance))

        # Remove name since we don't need it
        serialized_param.pop('name')

        # Get class path and uuid to save in InstanceModel
        class_path = self.get_class_path_from_param_instance(instance)
        new_instance_uuid = uuid.uuid4()
        new_instance = InstanceModel(id=str(new_instance_uuid), class_path=class_path)
        db_session.add(new_instance)

        param_models = list()
        for key, value in serialized_param.items():
            param_models.append(ParamModel(id=(str(uuid.uuid4())),
                                           value=json.dumps({'name': key, 'value': value,
                                                             'type': self.get_type_from_param_instance(instance, key)}),
                                           instance_id=str(new_instance_uuid)))

        for p in param_models:
            db_session.add(p)
        db_session.commit()

        return str(new_instance_uuid)

    @sqlalchemy_session
    def load(self, instance_id, **kwargs):
        """
        Load a parameterized instance from the database.

        Args:
            instance_id: The id corresponding to the row in the database for the parameterized instance to load.

        Returns:
            The parameterized instance populated from the database.
        """
        db_session = kwargs.get('db_session', None)
        instance_model = db_session.query(InstanceModel).filter_by(id=instance_id).first()
        param_models = db_session.query(ParamModel).filter_by(instance_id=instance_id)

        # Serialize data from param model
        param_model_serialized_data = self.load_serialized_data_from_param_model(param_models)

        # Getting param_object
        param_object = self.get_param_object_from_instance(instance_model)

        # Update param object with new data
        new_instance = self.update_param_object(param_object, param_model_serialized_data)

        return new_instance

    @sqlalchemy_session
    def delete(self, instance_id, **kwargs):
        """
        Delete a parameterized instance and its params from the database.

        Args:
            instance_id: The id of the parameterized instance to delete.
        """
        db_session = kwargs.get('db_session', None)

        instance_model = db_session.query(InstanceModel).get(instance_id)
        if instance_model is None:
            log.warning(f'unable to query database with given instance id. id="{instance_id}"')
            return
        db_session.delete(instance_model)
        db_session.commit()

    @sqlalchemy_session
    def update(self, instance, instance_id, **kwargs):
        """
        Update the rows in the database for a parameterized instance.

        Args:
            instance: The parameterized instance to update from.
            instance_id: The id of the parameterized instance in the database to update.

        Returns:
            The parameterized instance id.
        """
        db_session = kwargs.get('db_session', None)
        instance_model = db_session.query(InstanceModel).get(instance_id)
        if instance_model is None:
            raise RuntimeError(f'Parameterized instance with id "{instance_id}" does not exist.')
        serialized_param = json.loads(JSONSerialization.serialize_parameters(instance))
        serialized_param.pop('name')

        param_models_in_db = dict()
        for x in db_session.query(ParamModel).filter_by(instance_id=instance_id):
            param_models_in_db[x.id] = json.loads(x.value)

        params_in_instance = dict()
        for key, value in serialized_param.items():
            params_in_instance[key] = {'name': key, 'value': value,
                                       'type': self.get_type_from_param_instance(instance, key)}

        pids = [x for x in param_models_in_db.keys()]
        for pid in pids:
            param = param_models_in_db[pid]
            if param['name'] not in params_in_instance:
                continue
            param_model = db_session.query(ParamModel).get(pid)
            param_model.value = json.dumps(params_in_instance[param['name']])
            param_models_in_db.pop(pid)

        for param_model in param_models_in_db:
            param_model = db_session.query(ParamModel).get(param_model)
            db_session.delete(param_model)

        db_session.commit()

        return instance_id

    @staticmethod
    def get_param_names(param_object):
        """
        Return list of all the names in param.
        """
        param_items = param_object.get_param_values()
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
