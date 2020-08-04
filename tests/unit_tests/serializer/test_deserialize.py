"""
A Test param class for testing the serializer.

This file was created on August 04, 2020
"""
import pytest

from param_persist.serialize.serializer import ParamSerializer


def test_deserialize_from_dict():
    """
    Test the from_dict function of the serializer.
    """
    param_dict = {
        'class_path': 'tests.unit_tests.serializer.test_serialize.TestParam',
        'params': [
            {
                'name': 'number_field',
                'value': 1.7,
                'type': 'float',
            },
            {
                'name': 'integer_field',
                'value': 29,
                'type': 'int',
            },
            {
                'name': 'string_field',
                'value': 'Deserialize String',
                'type': 'str',
            },
            {
                'name': 'bool_field',
                'value': True,
                'type': 'bool',
            },
        ],
    }

    param_object = ParamSerializer.from_dict(param_dict)

    assert param_object.number_field == 1.7
    assert param_object.integer_field == 29
    assert param_object.string_field == 'Deserialize String'
    assert param_object.bool_field is True


def test_missing_class_path_in_dict():
    """
    Test the from_dict function of the serializer when missing the params.
    """
    param_dict = {
        'class_path': 'tests.unit_tests.serializer.test_serialize.TestParam',
    }

    with pytest.raises(RuntimeError) as excinfo:
        ParamSerializer.from_dict(param_dict)

    assert 'Param not configured correctly. Missing "params" definition.' in str(excinfo.value)


def test_bad_class_path_in_dict():
    """
    Test the from_dict function of the serializer when missing the params.
    """
    param_dict = {
        'class_path': 'this.path.does.not.exist.to.Class',
        'params': [
            {
                'name': 'number_field',
                'value': 1.7,
                'type': 'float',
            },
        ]
    }

    with pytest.raises(RuntimeError) as excinfo:
        ParamSerializer.from_dict(param_dict)

    assert 'Defined param class "class_path" was not importable. ' \
           'Given path is "this.path.does.not.exist.to.Class"' in str(excinfo.value)


def test_missing_params_in_dict():
    """
    Test the from_dict function of the serializer when missing the class path.
    """
    param_dict = {
        'params': [
            {
                'name': 'number_field',
                'value': 1.7,
                'type': 'float',
            },
            {
                'name': 'integer_field',
                'value': 29,
                'type': 'int',
            },
            {
                'name': 'string_field',
                'value': 'Deserialize String',
                'type': 'str',
            },
            {
                'name': 'bool_field',
                'value': True,
                'type': 'bool',
            },
        ],
    }

    with pytest.raises(RuntimeError) as excinfo:
        ParamSerializer.from_dict(param_dict)

    assert 'Param not configured correctly. Missing "class_path" definition.' in str(excinfo.value)


def test_deserialize_from_json():
    """
    Test the from_json function of the serializer.
    """
    param_json = '{"class_path": "tests.unit_tests.serializer.test_serialize.TestParam", ' \
                 '"params": [' \
                 '{"name": "bool_field", "value": true, "type": "bool"}, ' \
                 '{"name": "integer_field", "value": 29, "type": "int"}, ' \
                 '{"name": "number_field", "value": 1.7, "type": "float"}, ' \
                 '{"name": "string_field", "value": "Deserialize String", "type": "str"}' \
                 ']}'

    param_object = ParamSerializer.from_json(param_json)

    assert param_object.number_field == 1.7
    assert param_object.integer_field == 29
    assert param_object.string_field == 'Deserialize String'
    assert param_object.bool_field is True
