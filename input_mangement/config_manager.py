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

        schema = self.configuration_settings['schema']
        for sch_name in schema.keys():
            sch = schema[sch_name]
            sch_parameters = sch.keys()

            for parameter_name in sch_parameters:
                parameter = sch[parameter_name]
                for key in parameter.keys():
                    if key == 'type':
                        if parameter[key] not in ["const", "var"]:
                            raise TypeError(f'Values of field type of parameter {parameter["name"]} in schema {sch_name}'
                                            f' must be "const" or "var"')
        print("Configuration validated.")


class InputManager:
    def __init__(self, schema: dict, user_input: dict):
        self.schema = schema
        self.user_input = user_input

        self.input_validated = False

    def validate_input(self):
        for obj_name in self.user_input:
            obj_parameters = self.user_input[obj_name].keys()
            if "schema" not in obj_parameters:
                raise KeyError('Mandatory key "name" not found in the object')
            obj_schema_name = self.user_input[obj_name]["schema"]
            if obj_schema_name not in self.schema.keys():
                raise KeyError(f"Template {obj_schema_name} is no registered.")
            schema_template = self.schema[obj_schema_name]
            other_keys = [key for key in obj_parameters if key != "schema"]

            for key in other_keys:
                if key not in schema_template.keys():
                    raise KeyError(f'Key {key} provided in input is not present in schema')
            for key in schema_template.keys():
                if key not in other_keys:
                    raise KeyError(f'Key {key} provided not provided in input')
        self.input_validated = True
        print("Input validated.")

    def register_input(self):
        registry = []
        if not self.input_validated:
            raise RuntimeError("Input is not validated")
        i = 0
        for item in self.user_input:
            item_keys = [key for key in list(item.keys()) if key not in ["name", "schema"]]
            for key in item_keys:
                if self.schema[key]["type"] == "var":
                    registry.append(key)
