"""The __init__.py file for the models package in sqlalchemy.

This file was generated on July 30, 2020
"""
__author__ = "Gage Larsen"
__copyright__ = "Copyright: (c) Aquaveo 2020"
__maintainer__ = "Gage Larsen"
__email__ = "glarsen@aquaveo.com"

from sqlalchemy.ext.declarative import declarative_base

from param_persist.sqlalchemy.models.instance_model import InstanceModel  # NOQA: F401
from param_persist.sqlalchemy.models.param_model import ParamModel  # NOQA: F401


Base = declarative_base()
