import argparse

from utils.proccesor_handler import input_database_file, input_database_str
from utils.processors import DatabaseProcessor
from utils.processor_errors import ProcessorError


def main():
    # available actions
    actions = {
        "data_type": DatabaseProcessor.print_data_type_errors,
        "format_fields": DatabaseProcessor.print_format_fields_errors,
        "bus_info": DatabaseProcessor.print_bus_info,
        "stops_info": DatabaseProcessor.print_stops_info,
        "time_errors": DatabaseProcessor.print_arrival_time_errors,
        "demand_errors": DatabaseProcessor.print_demand_errors
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default=None,
                        help="Enter the path to the .json file with the data "
                             "otherwise it will be entered json-string through the console.")
    parser.add_argument("-v", "--verification", choices=actions.keys(),
                        help="Choice type of verification.")
    args = parser.parse_args()
    # input data
    if args.file:
        database_dict = input_database_file(args.file)
    else:
        database_dict = input_database_str()
    # process data
    db_bus_company = DatabaseProcessor(database_dict)
    action = actions[args.verification]
    try:
        action(db_bus_company)
    except ProcessorError as e:
        print(e)


if __name__ == "__main__":
    main()
