import pytest
import json

from unittest.mock import MagicMock
from input_management import ConfigurationManager


def test_load_configuration():
    config_manager = ConfigurationManager()

    with open('./configuration/config.json', 'r') as f:
        test_config = json.load(f)

    config_manager._validate_configuration = MagicMock()

    config_manager.load_configuration()
    config_manager._validate_configuration.assert_called_once_with()
    assert config_manager.configuration_settings == test_config


# Initialize some mock sets
mock_config_empty = {}
mock_config_incomplete_keys = {'input_method': 'stdin', 'stopping_criteria': '100'}
mock_config_incorrect_keywords = {'schema': {}, 'input_method': 'stdin', 'stopping_criteria': '100',
                                  'extra_key': 'no'}
mock_config_incorrect_parameter_types = {'schema': {'a': {'b': 'value'}}, 'input_method': 'stdin',
                                         'stopping_criteria': '100'}
mock_config_correct = {'schema': {'a': {'b': {'var_const': 'var'}}}, 'input_method': 'stdin',
                       'stopping_criteria': '100'}


def test_validate_configuration_empty():
    cm = ConfigurationManager()
    cm.configuration_settings = mock_config_empty
    with pytest.raises(ValueError) as exc_info:
        cm._validate_configuration()
    assert str(exc_info.value) == 'Configuration is empty'


def test_validate_configuration_incomplete_keys():
    cm = ConfigurationManager()
    cm.configuration_settings = mock_config_incomplete_keys
    with pytest.raises(TypeError) as exc_info:
        cm._validate_configuration()
    assert str(exc_info.value) == 'Configuration key words are incorrect'


def test_validate_configuration_correct():
    cm = ConfigurationManager()
    cm.configuration_settings = mock_config_correct
    try:
        cm._validate_configuration()
    except Exception as e:
        pytest.fail(f'Unexpected error occurred: {e}')
