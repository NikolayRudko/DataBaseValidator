from utils import input_database_file
from utils.processors import DatabaseProcessor


def main():
    # database_dict = input_database_str()
    database_dict = input_database_file("buses.json")
    database_bus_company = DatabaseProcessor(database_dict)
    # database_bus_company.check_demand()
    # database_bus_company.print_bus_info()
    # database_bus_company.print_stops_info()
    # database_bus_company.print_time_errors()
    database_bus_company.print_demand_errors()


if __name__ == "__main__":
    main()
