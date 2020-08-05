"""
Handlers used by the deserialize functions to get the correct types.

This file was created on August 04, 2020
"""


deserialize_handlers = {
    'param.Integer': lambda i: int(i),
    'param.Number': lambda f: float(f),
    'param.parameterized.String': lambda s: str(s),
    'param.Boolean': lambda b: bool(b),
}
