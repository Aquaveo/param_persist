WIP: param_persist
==================

![Main-CI Workflow](https://github.com/Aquaveo/param_persist/workflows/Main-CI/badge.svg)

This library will be used to persist param instance to databases, files or other persistent stores.

The current supported persist methods are:

- sqlalchemy database

This library so far requires the dev version of param. That can be installed by running the following:

```bash
python -m pip install git+https://github.com/holoviz/param.git
```

An jupyter notebook example of how to use the library can be found in the `examples` folder. 