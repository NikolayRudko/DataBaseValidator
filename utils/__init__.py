import json


def input_database_str() -> dict:
    """
    Read json-string from console, and return dict with data

    :return: dict with data
    """
    database = input()
    database_dict = json.loads(database)
    return database_dict


def input_database_file(file_name: str) -> dict:
    """
    Read *.json file and return dict with data

    :param file_name: Full path to the file you want to read.
    :return: dict with data
    """
    with open(file_name, "r") as json_file:
        database_dict = json.load(json_file)
    return database_dict
