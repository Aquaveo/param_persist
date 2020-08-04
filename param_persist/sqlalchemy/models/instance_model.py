"""
The instance model for the param sqlalchemy features.

This file was generated on July 30, 2020
"""
import uuid

from sqlalchemy import CHAR, Column, String
from sqlalchemy.orm import relationship

from param_persist.sqlalchemy.models import Base


class InstanceModel(Base):
    """
    The InstanceModel.
    """
    __tablename__ = 'instances'

    id = Column(CHAR(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    class_path = Column(String)

    params = relationship('ParamModel', back_populates='instance', cascade='all, delete, delete-orphan')

    def __repr__(self):
        """
        The __repr__ overloaded function.
        """
        return f'<Instance(id="{self.id}", class_path="{self.class_path}")>'
