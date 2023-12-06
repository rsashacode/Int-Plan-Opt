import json

from pathlib import Path


class ConfigurationManager:
    def __init__(self, config_filepath: Path):
        self.config_filepath = config_filepath
        self.configuration_settings = {}

    def load_configuration(self):
        with open(self.config_filepath, 'r') as j:
            self.configuration_settings = json.loads(j.read())
        self.validate_configuration()
        print("Configuration ready.")

    def validate_configuration(self):
        config_keys = self.configuration_settings.keys()

        if not self.configuration_settings:
            raise ValueError("Configuration is empty")

        if not all(['schema' in config_keys,
                    'input_method' in config_keys,
                    'stopping_criteria' in config_keys,
                    len(config_keys) == 3]):
            raise TypeError(f'Configuration key words are incorrect')

        schemas = self.configuration_settings['schema']
        for sch in schemas:
            ent_keys = sch.keys()
            if not all(['name' in ent_keys, 'parameters' in ent_keys, len(ent_keys) == 2]):
                raise TypeError('Entity schema key words are incorrect.')

            sch_name = sch['name']
            for parameter in sch['parameters']:
                for key in parameter.keys():
                    if key == 'name' and type(parameter[key]) != str:
                        raise TypeError(f'Name of parameter in schema {sch_name} is not string')
                    if key == 'type':
                        if parameter[key] not in ["const", "var"]:
                            raise TypeError(f'Values of field type of parameter {parameter["name"]} in schema {sch_name}'
                                            f' must be "const" or "var"')
        print("Configuration validated.")


class InputManager:
    def __init__(self, schema: dict):
        self.schema = schema
        self.schema_keys = self.schema.keys()

    def validate_input(self, input_: list[dict]):
        for item in input_:
            item_keys = item.keys()
            if "name" not in item_keys:
                raise KeyError('Mandatory key "name" not found in the object')
            other_keys = [key for key in item_keys if key != "name"]
            for key in other_keys:
                if key not in self.schema_keys:
                    raise KeyError(f'Key {key} provided in input is not present in schema')
        print("Input validated.")