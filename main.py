import json
import os

from optimizing import GeneticOptimizer
from input_management import ConfigurationManager, InputManager
from solution import SolutionHandler


def main():
    config_manager = ConfigurationManager()
    config_manager.load_configuration()

    schema = config_manager.configuration_settings["schema"]
    input_manger = InputManager(schema)

    if config_manager.configuration_settings['input_method'].lower() == 'json':
        if os.path.exists('./configuration/input.json'):
            with open('./configuration/input.json', 'r') as j:
                input_ = json.loads(j.read())
        else:
            raise FileNotFoundError('Input file not found.')
    else:
        # ToDo Start server!
        ...

    input_manger.register_input(input_)

    # initialise pygad
    go = GeneticOptimizer(
        solution_handler=SolutionHandler(input_manger),
        args_to_pygad=config_manager.configuration_settings['optimizer_settings'])
    go.optimize()
    print(go.result_list)


if __name__ == "__main__":
    main()