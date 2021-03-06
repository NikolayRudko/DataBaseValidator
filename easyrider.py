import argparse
import logging
import logging.handlers

from utils.processor_handler import input_database_file, input_database_str
from utils.processors import DatabaseProcessor
from utils.processor_errors import ProcessorError


def init_logger(name):
    logger = logging.getLogger(name)
    FORMAT = '%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    fh = logging.FileHandler(filename="logs/easyraider.log")
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.INFO)
    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.debug("logger was initialized")


init_logger("app")
logger = logging.getLogger("app.easyraider")


def main():
    # available actions
    actions = {
        "data_type": DatabaseProcessor.print_data_type_errors,
        "format_fields": DatabaseProcessor.print_format_fields_errors,
        "bus_info": DatabaseProcessor.print_bus_info,
        "stops_info": DatabaseProcessor.print_stops_info,
        "time_errors": DatabaseProcessor.print_arrival_time_errors,
        "demand_errors": DatabaseProcessor.print_demand_errors,
        "print_info": DatabaseProcessor.get_database
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default=None,
                        help="Enter the path to the .json file with the test_data "
                             "otherwise it will be entered json-string through the console.")
    parser.add_argument("-v", "--verification", choices=actions.keys(),
                        help="Choice type of verification.")
    args = parser.parse_args()

    try:
        # input test_data
        if args.file:
            database_dict = input_database_file(args.file)
            logger.info(f"File {args.file} was uploaded.")
        else:
            database_dict = input_database_str()
            logger.info('Console input.')
        # process test_data
        db_bus_company = DatabaseProcessor(database_dict)
        action = actions[args.verification]
        action(db_bus_company)
        logger.info(f"The {args.verification} has been run.")
    except ProcessorError as e:
        logger.warning(e)
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    logger.debug("Start processing...")
    main()
    logger.debug("End processing...")
