from input_mangement import ConfigurationManager
from pathlib import Path

CONFIG_PATH = Path('./config.json')


def main():
    config_manager = ConfigurationManager(CONFIG_PATH)
    config_manager.load_configuration()


if __name__ == "__main__":
    main()