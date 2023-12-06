import json

from input_mangement import ConfigurationManager, InputManager
from pathlib import Path

CONFIG_PATH = Path('./config.json')


def main():
    config_manager = ConfigurationManager(CONFIG_PATH)
    config_manager.load_configuration()

    with open('./test/input.json', 'r') as j:
        input_ = json.loads(j.read())

    schema = config_manager.configuration_settings["schema"]
    input_manger = InputManager(schema, input_)
    input_manger.validate_input()
    print()


if __name__ == "__main__":
    main()