import threading

from logs.log import logger
from flask import Flask, jsonify, request
from flasgger import Swagger
from input_management import ConfigurationManager, InputManager
from optimizing import GeneticOptimizer
from solution import SolutionHandler


class Server:
    """
    Creates a server if is set in configuration file

    """
    def __init__(self, config_manager: ConfigurationManager):
        logger.debug("Initializing Server")
        self.calculating = False
        self.calculated = False
        self.app = Flask(__name__)
        self.swagger = Swagger(self.app)

        self.config_manager = config_manager
        self.schema = self.config_manager.configuration_settings["schema"]
        self.input_manager = InputManager(self.schema)
        self.optimizer = None

        self.app.add_url_rule('/', 'home', self.home, methods=['GET'])
        self.app.add_url_rule('/input', 'input', self.input, methods=['POST'])
        self.app.add_url_rule('/start', 'start', self.start_calculation, methods=['GET'])
        self.app.add_url_rule('/status', 'status', self.status, methods=['GET'])
        logger.debug("Server successfully initialised.")

    def do_calculation(self):
        """
        Starts the calculation. Should be called in a separate thread.

        :return:
        """
        logger.info("Starting calculation")
        if self.config_manager.configuration_settings['fitness_function'] != 'included':
            external_fitness = True
        else:
            external_fitness = False
        self.optimizer = GeneticOptimizer(
            solution_handler=SolutionHandler(self.input_manager),
            args_to_pygad=self.config_manager.configuration_settings['optimizer_settings'],
            external_fitness_function=external_fitness
        )
        self.calculating = True
        self.optimizer.optimize()
        self.optimizer.save_results()
        self.calculating = False
        self.calculated = True
        logger.info("Calculation successful.")

    def input(self):
        """
        This endpoint expects an object of the same schema as defined globally and starts calculations
        ---
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
        responses:
          200:
            description: Input received
        """
        input_data = request.get_json()
        logger.info("Input data received")
        if not self.calculating:
            self.input_manager.register_input(input_data)
            return jsonify({"message": "Accepted input."}), 200
        else:
            return jsonify({"message": "Calculation is already running"}), 200

    def start_calculation(self):
        """
        This endpoint starts calculations
        ---
        responses:
          200:
            description: Calculation started
        """
        if not self.calculating:
            threading.Thread(target=self.do_calculation).start()
            return jsonify({"message": "Calculation has successfully started"}), 200
        else:
            return jsonify({"message": "Calculation is already running"}), 200

    def status(self):
        """
        This endpoint provides the current status of calculation
        ---
        responses:
          200:
            description: Status of the calculations
        """
        if self.calculating:
            return jsonify({"status": "Calculating"}), 200
        elif self.calculated:
            return jsonify({"status": "Calculation complete",
                            "best_fitness": self.optimizer.solution_fitness,
                            "best_result": self.optimizer.result_list}), 200
        else:
            return jsonify({"status": "Idle"}), 200

    def home(self):
        return jsonify({"message": "Server is running"}), 200

    def start(self):
        self.app.run(debug=False, host='0.0.0.0', port=5000)
