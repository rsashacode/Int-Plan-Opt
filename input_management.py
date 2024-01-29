import json
from logs.log import logger

class ConfigurationManager:
    """
    Configuration manager. This class is responsible for managing the configuration of the program.

    """
    def __init__(self):
        self.configuration_settings = {}
        self.schema = {}

    def load_configuration(self):
        """
        Load configuration from json file.

        :return:
        """
        with open('./configuration/config.json', 'r') as j:
            self.configuration_settings = json.loads(j.read())
        self._validate_configuration()
        logger.info("Configuration ready.")

    def _validate_configuration(self):
        """
        Validate configuration. Checks if the necessary keys are present in it.

        :return:
        """
        config_keys = self.configuration_settings.keys()

        if not self.configuration_settings:
            logger.error("Configuration is empty")
            raise ValueError("Configuration is empty")

        if not all(['schema' in config_keys,
                    'input_method' in config_keys,
                    'stopping_criteria' in config_keys]):
            logger.error(f'Configuration key words are incorrect')
            raise TypeError(f'Configuration key words are incorrect')

        schema = self.configuration_settings['schema']
        for sch_name in schema.keys():
            sch = schema[sch_name]
            sch_parameters = sch.keys()

            for parameter_name in sch_parameters:
                parameter_type = sch[parameter_name]['var_const']
                if parameter_type not in ["const", "var"]:
                    logger.error(f'Type of parameter {parameter_name} in schema {sch_name}'
                                    f' must be "const" or "var"')
                    raise TypeError(f'Type of parameter {parameter_name} in schema {sch_name}'
                                    f' must be "const" or "var"')
        self.schema = schema
        logger.info("Configuration validated.")


class InputManager:
    """
    This class is responsible for all operations related to input data.

    """
    def __init__(self, schema: dict):
        self.schema = schema
        self.user_input = None

        self.input_validated = False
        self.indexes_assigned = False

        self.index_to_parameter = {}
        self.index_to_gene_space = {}
        self.index_to_gene_type = {}
        self.parameter_to_index = {}

        self.gene_space = []
        self.gene_type = []

    def register_input(self, input_dict: dict):
        """
        Register input in the class.

        :param input_dict: input dictionary. must be same structure as provided schema.
        :return:
        """
        self.user_input = input_dict
        self._validate_input()
        self._allocate_indexes()
        self._create_gene_space()
        logger.info("Registered input")

    def _validate_input(self):
        """
        Validate input and necessary keys.

        :return:
        """
        for obj_name in self.user_input:
            obj_parameters = self.user_input[obj_name].keys()
            if "schema" not in obj_parameters:
                logger.error('Mandatory key "schema" not found in the object')
                raise KeyError('Mandatory key "schema" not found in the object')
            obj_schema_name = self.user_input[obj_name]["schema"]
            if obj_schema_name not in self.schema.keys():
                logger.error(f"Template {obj_schema_name} is no registered.")
                raise KeyError(f"Template {obj_schema_name} is not registered.")
            schema_template = self.schema[obj_schema_name]
            other_keys = [key for key in obj_parameters if key != "schema"]

            for key in other_keys:
                if key not in schema_template.keys():
                    logger.error(f'Key {key} provided in input is not present in schema')
                    raise KeyError(f'Key {key} provided in input is not present in schema')
            for key in schema_template.keys():
                if key not in other_keys:
                    logger.error(f'Key {key} provided not provided in input')
                    raise KeyError(f'Key {key} provided not provided in input')
        self.input_validated = True
        logger.info("Input validated.")

    def __process_schema_parameter(self, gene_index: int, schema_parameter: dict):
        """
        Processing each parameter. Determination of its type and gene space.

        :param gene_index: index of the gene
        :param schema_parameter: parameter of the schema.
        :return:
        """
        gene_space_dict = {}

        # Check if 'type' is in schema_parameter
        gene_type = schema_parameter.get('type')
        if gene_type not in [None, "int", "float", "binary"]:
            logger.error(f'Gene type {gene_type} is not in ["int", "binary", "float"]')
            raise TypeError(f'Gene type {gene_type} is not in ["int", "binary", "float"]')

        # Check if 'range_low' and 'range_high' are both present if either is present
        range_low = schema_parameter.get("range_low")
        range_high = schema_parameter.get("range_high")
        if range_low is not None or range_high is not None:
            if range_low is None or range_high is None:
                logger.error("Both 'range_low' and 'range_high' must be present")
                raise KeyError("Both 'range_low' and 'range_high' must be present")

            # Validate types based on gene_type
            if gene_type == 'int':
                if not isinstance(range_low, int) or not isinstance(range_high, int):
                    logger.error("For 'int' type, 'range_low' and 'range_high' must be integers")
                    raise TypeError("For 'int' type, 'range_low' and 'range_high' must be integers")

            elif gene_type == 'binary':
                if range_low != 0 or range_high != 1:
                    logger.error("For 'binary' type, 'range_low' must be 0 and 'range_high' must be 1")
                    raise TypeError("For 'binary' type, 'range_low' must be 0 and 'range_high' must be 1")

        # Set values in gene_space_dict
        if gene_type == 'binary':
            self.index_to_gene_type[gene_index] = int
            gene_space_dict = {"low": 0, "high": 1, "step": 1}
        elif gene_type in ['int', 'float']:
            gene_space_dict["low"] = range_low
            gene_space_dict["high"] = range_high
            if gene_type == 'int':
                self.index_to_gene_type[gene_index] = int
                gene_space_dict["step"] = 1
            else:
                self.index_to_gene_type[gene_index] = float

        if range_low is None and range_high is None:
            gene_space_dict = None
        self.index_to_gene_space[gene_index] = gene_space_dict
        logger.debug(f"{gene_index}_registered")

    def _allocate_indexes(self):
        """
        Allocate indexes for each parameter to put it in gene space.

        :return:
        """
        i = 0
        for user_object_name in self.user_input.keys():
            user_object = self.user_input[user_object_name]
            parameter_to_index_object = {}
            for parameter in user_object.keys():
                if parameter != 'schema':
                    schema_parameter = self.schema[user_object["schema"]][parameter]
                    if schema_parameter["var_const"] == 'var':
                        self.index_to_parameter[i] = {"name": user_object_name, 'parameter': parameter}
                        self.__process_schema_parameter(i, schema_parameter)
                        parameter_to_index_object[parameter] = i
                        i += 1
            self.parameter_to_index[user_object_name] = parameter_to_index_object
        self.indexes_assigned = True
        logger.debug("Indexes allocated")

    def _create_gene_space(self):
        """
        Generate gene space to speed up the calculations.

        :return:
        """
        if self.indexes_assigned:
            if (list(self.index_to_gene_space.keys()) == [i for i in range(len(self.index_to_gene_space))] and
                    list(self.index_to_gene_type.keys()) == [i for i in range(len(self.index_to_gene_type))]):
                self.gene_space = [item[1] for item in self.index_to_gene_space.items()]
                self.gene_type = [item[1] for item in self.index_to_gene_type.items()]
            else:
                logger.error("Gene space incorrectly assigned")
                raise RuntimeError("Gene space incorrectly assigned")
        else:
            logger.error("Indexes not assigned")
            raise RuntimeError('Indexes not assigned')
        logger.debug("Gene space created")
