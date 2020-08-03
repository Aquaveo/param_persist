from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from param_persist.sqlalchemy.models.instance_model import InstanceModel  # NOQA: F401, E402
from param_persist.sqlalchemy.models.param_model import ParamModel  # NOQA: F401, E402
