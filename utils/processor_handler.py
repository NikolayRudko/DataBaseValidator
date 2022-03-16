import json
import logging

logger = logging.getLogger("app.utils.processor_handler")

def input_database_str() -> list:
    """
    Read json-string from console, and return dict with test_data

    :return: dict with test_data
    """
    while True:
        database = input("Input json string:")
        try:
            database_dict = json.loads(database)
        except Exception as e:
            print(e)
            print("Invalid input")
            logger.warning(e)
            continue
        return database_dict


def input_database_file(file_name: str) -> list:
    """
    Read *.json file and return dict with test_data

    :param file_name: Full path to the file you want to read.
    :return: dict with test_data
    """
    with open(file_name, "r") as json_file:
        database_dict = json.load(json_file)
    return database_dict
