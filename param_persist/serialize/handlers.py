"""
Handlers for getting and setting data from and on param classes.

This file was created on August 03, 2020
"""
import param

param_serialize_handlers = {
    param.Number: lambda f: float(f),
    param.Integer: lambda i: int(i),
    param.Boolean: lambda b: bool(b),
    param.String: lambda s: str(s),
}
