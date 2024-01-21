import json

from pathlib import Path


class ConfigurationManager:
    def __init__(self, config_filepath: Path):
        self.config_filepath = config_filepath
        self.configuration_settings = {}
        self.schema = {}

    def load_configuration(self):
        with open(self.config_filepath, 'r') as j:
            self.configuration_settings = json.loads(j.read())
        self._validate_configuration()
        print("Configuration ready.")

    def _validate_configuration(self):
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
                parameter_type = sch[parameter_name]['var_const']
                if parameter_type not in ["const", "var"]:
                    raise TypeError(f'Type of parameter {parameter_name} in schema {sch_name}'
                                    f' must be "const" or "var"')
        self.schema = schema
        print("Configuration validated.")


class InputManager:
    def __init__(self, schema: dict, user_input: dict):
        self.schema = schema
        self.user_input = user_input

        self.input_validated = False

        self.index_to_parameter = {}
        self.index_to_gene_space = {}
        self.parameter_to_index = {}

        self.gene_space = []

    def register_input(self):
        self._validate_input()
        self._allocate_indexes()

    def _validate_input(self):
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

    def __process_schema_parameter(self, gene_index: int, schema_parameter: dict):
        gene_space_dict = {}

        # Check if 'type' is in schema_parameter
        gene_type = schema_parameter.get('type')
        if gene_type not in [None, "int", "float", "binary"]:
            raise TypeError(f'Gene type {gene_type} is not in ["int", "binary", "float"]')

        # Check if 'range_low' and 'range_high' are both present if either is present
        range_low = schema_parameter.get("range_low")
        range_high = schema_parameter.get("range_high")
        if range_low is not None or range_high is not None:
            if range_low is None or range_high is None:
                raise KeyError("Both 'range_low' and 'range_high' must be present")

            # Validate types based on gene_type
            if gene_type == 'int':
                if not isinstance(range_low, int) or not isinstance(range_high, int):
                    raise TypeError("For 'int' type, 'range_low' and 'range_high' must be integers")
            elif gene_type == 'binary':
                if range_low != 0 or range_high != 1:
                    raise TypeError("For 'binary' type, 'range_low' must be 0 and 'range_high' must be 1")

        # Set values in gene_space_dict
        if gene_type == 'binary':
            gene_space_dict = {"low": 0, "high": 1, "step": 1}
        elif gene_type in ['int', 'float']:
            gene_space_dict["low"] = range_low
            gene_space_dict["high"] = range_high
            if gene_type == 'int':
                gene_space_dict["step"] = 1

        self.index_to_gene_space[gene_index] = gene_space_dict

    def _allocate_indexes(self):
        i = 0
        for user_object_name in self.user_input.keys():
            user_object = self.user_input[user_object_name]
            parameter_to_index_object = {}
            for parameter in user_object.keys():
                if parameter != 'schema':
                    schema_parameter = self.schema[user_object["schema"]][parameter]
                    if schema_parameter["var_const"] == 'var':
                        self.index_to_parameter[i] = {"name": user_object_name, parameter: parameter}
                        self.__process_schema_parameter(i, schema_parameter)
                        parameter_to_index_object[parameter] = i
                        i += 1
            self.parameter_to_index[user_object_name] = parameter_to_index_object
        print("Indexes allocated")
