import pytest

from input_management import InputManager


@pytest.fixture
def input_manager():
    schema = {
        'param_1': {
            'type': 'int',
            'range_low': 0,
            'range_high': 100
        },
        'param_2': {
            'type': 'float',
            'range_low': 0.0,
            'range_high': 1.0
        }
    }
    return InputManager(schema)


def test_register_input_invalid(input_manager):
    input_dict = {
        'param_1': "invalid_type",
        'param_2': 0.5
    }
    with pytest.raises(Exception):
        input_manager.register_input(input_dict)


def test_register_input_missing_param(input_manager):
    input_dict = {
        'param_1': 50
    }
    with pytest.raises(Exception):
        input_manager.register_input(input_dict)


def test_register_input_extra_param(input_manager):
    input_dict = {
        'param_1': 50,
        'param_2': 0.5,
        'param_3': "extra_param"
    }
    with pytest.raises(Exception):
        input_manager.register_input(input_dict)


def test_register_input_out_of_range(input_manager):
    input_dict = {
        'param_1': 101,
        'param_2': 1.1
    }
    with pytest.raises(Exception):
        input_manager.register_input(input_dict)


def test_process_schema_parameter_with_invalid_type():
    im = InputManager({})
    with pytest.raises(TypeError):
        im._process_schema_parameter(1, {"type": "str"})


def test_process_schema_parameter_with_nullable_ranges():
    im = InputManager({})
    with pytest.raises(KeyError):
        im._process_schema_parameter(1, {"type": "int", "range_low": 1})


def test_process_schema_parameter_with_invalid_int_ranges():
    im = InputManager({})
    with pytest.raises(TypeError):
        im._process_schema_parameter(1, {"type": "int", "range_low": "1", "range_high": 2})


def test_process_schema_parameter_with_invalid_binary_ranges():
    im = InputManager({})
    with pytest.raises(TypeError):
        im._process_schema_parameter(1, {"type": "binary", "range_low": 0, "range_high": 2})


def test_process_schema_parameter_with_valid_int():
    im = InputManager({})
    assert im._process_schema_parameter(1, {"type": "int", "range_low": 1, "range_high": 5}) is None


def test_process_schema_parameter_with_valid_float():
    im = InputManager({})
    assert im._process_schema_parameter(1, {"type": "float", "range_low": 1.0, "range_high": 3.0}) is None


def test_process_schema_parameter_with_valid_binary():
    im = InputManager({})
    assert im._process_schema_parameter(1, {"type": "binary", "range_low": 0, "range_high": 1}) is None

def test_allocate_indexes():
    # Define schema and user_input to cover different paths
    schema = {
        "schema1": {
            "param1": {"var_const": 'var'},
            "param2": {"var_const": 'const'}
        },
        "schema2": {
            "param3": {"var_const": 'var'},
            "param4": {"var_const": 'var'}
        }
    }

    user_input = {
        "object1": {"schema": "schema1", "param1": 5, "param2": 10},
        "object2": {"schema": "schema2", "param3": 3, "param4": 7}
    }

    manager = InputManager(schema)
    manager.register_input(user_input)

    manager._allocate_indexes()

    assert manager.index_to_parameter == {0: {"name": "object1", "parameter": "param1"},
                                          1: {"name": "object2", "parameter": "param3"},
                                          2: {"name": "object2", "parameter": "param4"}}

    assert manager.parameter_to_index == {"object1": {"param1": 0},
                                          "object2": {"param3": 1, "param4": 2}}

    assert manager.indexes_assigned