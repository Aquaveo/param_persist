"""
Class for serializing param data.

This file was created on August 03, 2020
"""
import importlib
import json

from param_persist.serialize.handlers import deserialize_handlers


class ParamSerializer(object):
    """
    A class used to serialize a param class.
    """
    @classmethod
    def to_dict(cls, parameterized_object):
        """
        Serialize a param object to a dictionary.

        Args:
            parameterized_object: The param object to be serialized.

        Returns:
            A dictionary populated from values in a param object.
        """
        class_path = ".".join([
            parameterized_object.__module__,
            parameterized_object.__class__.__name__,
        ])
        param_names, param_values = cls._param_class_to_names_values(parameterized_object)

        param_list = []
        for i in range(0, len(param_names)):
            param_list.append(
                {
                    'name': param_names[i],
                    'value': param_values[i],
                    'type': param_values[i].__class__.__name__,
                }
            )
        param_dict = {
            'class_path': class_path,
            'params': param_list,
        }
        return param_dict

    @classmethod
    def to_json(cls, param_object):
        """
        Serialize a param object to a json string.

        Args:
            param_object: The param object to be serialized.

        Returns:
            A json string populated from values in a param object.
        """
        param_dict = cls.to_dict(param_object)
        param_json = json.dumps(param_dict)
        return param_json

    @classmethod
    def from_dict(cls, param_dict):
        """
        Create an instance of a param clam from a dictionary.

        Args:
            param_dict (dict): A dictionary representation of a param class.

        Returns:
            An instance of a param class defined by the dictionary.
        """
        class_path = param_dict.get('class_path')

        if not class_path:
            raise RuntimeError('Param not configured correctly. Missing "class_path" definition.')

        dict_params = param_dict.get('params')

        if not dict_params:
            raise RuntimeError('Param not configured correctly. Missing "params" definition.')

        try:
            class_base_path, class_name = class_path.rsplit('.', 1)
            param_module = importlib.import_module(class_base_path)
            param_class = getattr(param_module, class_name)
        except ImportError:
            raise RuntimeError(f'Defined param class "class_path" was not importable. Given path is "{class_path}"')

        param_object = param_class()

        for item in dict_params:
            handler = deserialize_handlers[item['type']]
            setattr(param_object, item['name'], handler(item['value']))

        return param_object

    @classmethod
    def from_json(cls, param_json):
        """
        Create an instance of a param class from json string.

        Args:
            param_json (str): A json string representation of a param class.

        Returns:
            An instance of a param class defined by the json string.
        """
        param_dict = json.loads(param_json)
        param_instance = cls.from_dict(param_dict)
        return param_instance

    @staticmethod
    def _param_class_to_names_values(param_class):
        """
        Returns a list of param names and values.

        Args:
           param_class (param.Parameterized): class with param objects

        Return:
            names(list(str)), values(list(values))
        """
        cls_name = param_class.__class__.__name__
        pnames, params = ParamSerializer._names_and_params_from_class(param_class)
        cls_list = [(cls_name, pnames, params, param_class)]

        names = []
        values = []
        for item in cls_list:
            par_cls = item[3]
            for i in range(len(item[1])):
                name = item[1][i]
                val = getattr(par_cls, name)
                names.append(f'{name}')
                values.append(val)
        return names, values

    @staticmethod
    def _names_and_params_from_class(param_class):
        """
        Returns a list of param names and objects.

        Args:
           param_class (param.Parameterized): class with param objects

        Return:
            names(list(str)), params(list(param objects)
        """
        names = []
        params = []
        p = param_class.param
        lst = p.get_param_values()
        for item in lst:
            if item[0] in ['name']:
                continue
            obj = getattr(p, item[0])
            if obj is not None:
                names.append(item[0])
                params.append(obj)
        return names, params
