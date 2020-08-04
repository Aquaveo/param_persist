"""
Class for serializing param data.

This file was created on August 03, 2020
"""
import json


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
            cls_name = item[0]
            par_cls = item[3]
            for i in range(len(item[1])):
                name = item[1][i]
                val = getattr(par_cls, name)
                names.append(f'{cls_name}.{name}')
                values.append(val)
        return names, values

    @staticmethod
    def _names_and_params_from_class(param_class):
        """Returns a list of param names and objects.

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
