"""
The param model for the param sqlalchemy features.

This file was generated on July 30, 2020
"""
import uuid

from sqlalchemy import CHAR, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from . import Base


class ParamModel(Base):
    """
    The ParamModel.
    """
    __tablename__ = 'params'

    id = Column(CHAR(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    instance_id = Column(String, ForeignKey('instances.id'))
    value = Column(String)

    instance = relationship('InstanceModel', back_populates='params')

    def __repr__(self):
        """
        The __repr__ overloaded function.
        """
        return f'<Param(id="{self.id}", instance_id="{self.instance_id}")>'
