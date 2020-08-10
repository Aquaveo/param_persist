"""
The SqlAlchemy Engine

This file was created on August 05, 2020
"""
import json
import uuid

from param_persist.agents.base import AgentBase
from param_persist.serialize.serializer import ParamSerializer
from param_persist.sqlalchemy.models import InstanceModel, ParamModel
from sqlalchemy.orm import sessionmaker


class SqlAlchemyAgent(AgentBase):

    def __init__(self, engine):
        super().__init__(engine)
        self.session_maker = sessionmaker(bind=self.engine)

    def save(self, instance):
        db_session = self.session_maker()

        try:
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

        except Exception:
            db_session.rollback()
            raise
        finally:
            db_session.close()
        return str(new_instance_uuid)

    def load(self, instance_id):
        db_session = self.session_maker()

        try:
            instance_model = db_session.query(InstanceModel).filter_by(id=instance_id).first()
            param_models = db_session.query(ParamModel).filter_by(instance_id=instance_id)
            param_models_json = [x.value for x in param_models]
            param_models_joined_json = ", ".join(param_models_json).replace("'", '"')
            parameterized_json = '{' \
                                 f'  "class_path": "{instance_model.class_path}",' \
                                 f'  "params": [{param_models_joined_json}]' \
                                 '}'
            new_instance = ParamSerializer.from_json(parameterized_json)

        except Exception:
            db_session.rollback()
            raise
        finally:
            db_session.close()

        return new_instance


    def delete(self, instance_id):
        pass

    def update(self, instance, instance_id):
        pass

    @staticmethod
    def _names_and_params_from_class(param_class):
        """
        Returns a list of param names and objects.

        Args:
           param_class (param.Parameterized): class with param objects

        Return:
            names(list(str)), params(list(param objects)
        """
        names = []
        params = []
        p = param_class.param
        lst = p.get_param_values()
        for item in lst:
            if item[0] in ['name']:
                continue
            obj = getattr(p, item[0])
            if obj is not None:
                names.append(item[0])
                params.append(obj)
        return names, params