"""
Tests for testing the serialize methods of the serializer.

This file was created on August 03, 2020
"""
import param

from param_persist.serialize.serializer import ParamSerializer


class TestParam(param.Parameterized):
    """
    A Test param class for testing the serializer.
    """
    number_field = param.Number(0.5, doc="A simple number field.")
    integer_field = param.Integer(1, doc="A simple integer field.")
    string_field = param.String("My String", doc="A simple string field.")
    bool_field = param.Boolean(False, doc="A simple boolean field.")


def test_serialize_to_dict():
    """
    Test the to_dict function of the serializer.
    """
    param_object = TestParam()
    serialized_dict = ParamSerializer.to_dict(param_object)

    expected = {
        'class_path': 'tests.unit_tests.serializer.test_serialize.TestParam',
        'params': [
            {
                'name': 'number_field',
                'value': 0.5,
                'type': 'float',
            },
            {
                'name': 'integer_field',
                'value': 1,
                'type': 'int',
            },
            {
                'name': 'string_field',
                'value': 'My String',
                'type': 'str',
            },
            {
                'name': 'bool_field',
                'value': False,
                'type': 'bool',
            },
        ],
    }

    assert serialized_dict.get('class_path') == expected.get('class_path')
    assert len(serialized_dict.get('params')) == len(expected.get('params'))
    for i in serialized_dict.get('params'):
        assert i in expected.get('params')


def test_serialize_to_json():
    """
    Test the to_json function of the serializer.
    """
    param_object = TestParam()
    serialized_json = ParamSerializer.to_json(param_object)

    expected = '{"class_path": "tests.unit_tests.serializer.test_serialize.TestParam", ' \
               '"params": [' \
               '{"name": "bool_field", "value": false, "type": "bool"}, ' \
               '{"name": "integer_field", "value": 1, "type": "int"}, ' \
               '{"name": "number_field", "value": 0.5, "type": "float"}, ' \
               '{"name": "string_field", "value": "My String", "type": "str"}' \
               ']}'

    assert serialized_json == expected
