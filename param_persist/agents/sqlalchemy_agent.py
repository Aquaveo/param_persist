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
        pass

    def delete(self, instance_id):
        pass

    def update(self, instance, instance_id):
        pass