"""
The SqlAlchemy Agent.

This file was created on August 05, 2020
"""
import json
import logging
import uuid

from sqlalchemy.orm import sessionmaker

from param_persist.agents.base import AgentBase
from param_persist.serialize.serializer import ParamSerializer
from param_persist.sqlalchemy.models import InstanceModel, ParamModel


log = logging.getLogger('param_persist')


def sqlalchemy_session(wrapped_function):
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
        serialized_param_dict = ParamSerializer.to_dict(instance)
        new_instance_uuid = uuid.uuid4()
        new_instance = InstanceModel(id=str(new_instance_uuid), class_path=serialized_param_dict.get('class_path'))
        db_session.add(new_instance)

        param_models = [ParamModel(id=(str(uuid.uuid4())), value=json.dumps(param),
                                   instance_id=str(new_instance_uuid))
                        for param in serialized_param_dict.get('params', [])]

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
        param_models_json = [x.value for x in param_models]
        param_models_joined_json = ", ".join(param_models_json).replace("'", '"')
        parameterized_json = '{' \
                             f'  "class_path": "{instance_model.class_path}",' \
                             f'  "params": [{param_models_joined_json}]' \
                             '}'
        new_instance = ParamSerializer.from_json(parameterized_json)

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

        serialized_param_dict = ParamSerializer.to_dict(instance)
        instance_model.class_path = serialized_param_dict.get('class_path')

        param_models_in_db = {
            x.id: json.loads(x.value)
            for x in db_session.query(ParamModel).filter_by(instance_id=instance_id)
        }
        params_in_instance = {x['name']: x for x in serialized_param_dict.get('params', [])}

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
