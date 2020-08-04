"""
Handlers used by the deserialize functions to get the correct types.

This file was created on August 04, 2020
"""

deserialize_handlers = {
    'int': lambda i: int(i),
    'float': lambda f: float(f),
    'str': lambda s: str(s),
    'bool': lambda b: bool(b),
}
