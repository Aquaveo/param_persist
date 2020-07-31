"""The instance model for the param sqlalchemy features.

This file was generated on July 30, 2020
"""
__author__ = "Gage Larsen"
__copyright__ = "Copyright: (c) Aquaveo 2020"
__maintainer__ = "Gage Larsen"
__email__ = "glarsen@aquaveo.com"

import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from . import Base


class InstanceModel(Base):
    """The InstanceModel."""
    __tablename__ = 'instances'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    class_name = Column(String)

    params = relationship('ParamModel', back_populates='instance', cascade='all, delete, delete-orphan')

    def __repr__(self):
        """The __repr__ overloaded function."""
        return f'<Instance(id="{self.id}", class_name="{self.class_name}")>'