from logs.log import logger
from service_management import Service


def main():
    """
    Main function to start the service.
    :return:
    """
    logger.info("Starting Int-Plan-Opt")
    service = Service()
    if not service.server_status:
        service.start_optimization()


if __name__ == "__main__":
    main()
