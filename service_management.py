import json
import os

from optimizing import GeneticOptimizer
from input_management import ConfigurationManager, InputManager
from solution import SolutionHandler
from server.server import Server
from logs.log import logger

class Service:
    """
    Master class handling the service behaviour.

    """
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.config_manager.load_configuration()

        if self.config_manager.configuration_settings['input_method'].lower() == 'json':
            if os.path.exists('./configuration/input.json'):
                with open('./configuration/input.json', 'r') as j:
                    input_ = json.loads(j.read())
                self.schema = self.config_manager.configuration_settings["schema"]
                self.input_manger = InputManager(self.schema)
                self.input_manger.register_input(input_)
                self.go = GeneticOptimizer(
                    solution_handler=SolutionHandler(self.input_manger),
                    args_to_pygad=self.config_manager.configuration_settings['optimizer_settings'])
            else:
                logger.error("Input file not found.")
                raise FileNotFoundError('Input file not found.')
        else:
            server = Server(self.config_manager)
            server.start()

    def start_optimization(self):
        """
        Start the service.

        :return:
        """
        self.go.optimize()
        self.go.save_results()
        logger.info(self.go.result_list)
