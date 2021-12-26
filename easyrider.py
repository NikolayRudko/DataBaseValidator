import json
import re


class DataBase:
    def __init__(self, database):
        self.database = database
        self.format_errors = dict(stop_name=0, stop_type=0, a_time=0)
        self.total_format_errors = 0
        self.type_errors = dict(bus_id=0, stop_id=0, stop_name=0, next_stop=0, stop_type=0, a_time=0)
        self.total_type_errors = 0
        self.bus_info = {}

    def check_data_type(self) -> None:
        data_type = dict(bus_id=int, stop_id=int, stop_name=str, next_stop=int, stop_type=str, a_time=str)
        required_fields = ["stop_name", 'a_time']
        for i in self.database:
            for k, v in i.items():
                if type(v) != data_type[k]:
                    self.type_errors[k] += 1
                    continue
                if k == "stop_type" and not re.match(r"^.?$", v):
                    self.type_errors[k] += 1
                if k in required_fields and v == "":
                    self.type_errors[k] += 1
        self.total_type_errors = 0
        for err in self.type_errors.values():
            self.total_type_errors += err

    def print_data_type_errors(self) -> None:
        self.check_data_type()
        print(f"Type and required field validation: {self.total_type_errors} errors")
        for k, v in self.type_errors.items():
            print(f'{k}: {v}')

    def check_format_fields(self) -> None:
        validation_fields = dict(stop_name=re.compile(r"^([A-Z]\w+ )+(Road|Avenue|Boulevard|Street)$"),
                                 stop_type=re.compile(r"^[SOF]?$"),
                                 a_time=re.compile(r"^([01]\d|2[0-3])(:)([0-5]\d)$"))
        for i in self.database:
            for k, v in i.items():
                if k in validation_fields and not validation_fields[k].match(v):
                    self.format_errors[k] += 1
        self.total_format_errors = 0
        for err in self.format_errors.values():
            self.total_format_errors += err

    def print_format_fields_errors(self) -> None:
        self.check_format_fields()
        print(f"Format validation: {self.total_format_errors} errors")
        for k, v in self.format_errors.items():
            print(f'{k}: {v}')

    def calculate_stops(self):
        for i in self.database:
            bus_id = i['bus_id']
            if bus_id not in self.bus_info:
                self.bus_info[bus_id] = {"start": [], "stops": [], "finish": []}
            stop_info = (i["stop_name"], i["a_time"])
            self.bus_info[bus_id]["stops"].append(stop_info)
            if i["stop_type"] == "S":
                self.bus_info[bus_id]["start"].append(stop_info)
            elif i["stop_type"] == "F":
                self.bus_info[bus_id]["finish"].append(stop_info)

    def print_bus_info(self) -> None:
        self.calculate_stops()
        print("Line names and number of stops:")
        for bus, stops in self.bus_info.items():
            print(f'bus_id: {bus}, stops: {len(stops["stops"])}')

    def find_transfer_stops(self):
        self.calculate_stops()
        transfer_stops = set()
        for bus, stops in self.bus_info.items():
            for b, s in self.bus_info.items():
                if bus != b:
                    first_line = set([i[0] for i in stops["stops"]])
                    second_line = set([i[0] for i in s["stops"]])
                    crossover = first_line.intersection(second_line)
                    if crossover:
                        transfer_stops.update(crossover)
        return transfer_stops

    #
    # def print_bus_info(self):
    #     self.calculate_stops()
    #     start_stops = set()
    #     finish_stops = set()
    #
    #     for k, v in self.bus_info.items():
    #         if len(v['start']) != 1 or len(v["finish"]) != 1:
    #             print(f'There is no start or end stop for the line: {k}.')
    #             break
    #         else:
    #             start_stops.update(v["start"])
    #             finish_stops.update(v["finish"])
    #     else:
    #         transfer_stops = self.find_transfer_stops()
    #         print(f'Start stops: {len(start_stops)} {sorted(list(start_stops))}')
    #         print(f'Transfer stops: {len(transfer_stops)} {sorted(list(transfer_stops))}')
    #         print(f'Finish stops: {len(finish_stops)} {sorted(list(finish_stops))}')

    def check_time(self):
        self.calculate_stops()
        errors = []
        for bus_name, bus in self.bus_info.items():
            previous_time = 0
            for name, time in bus["stops"]:
                hours, minutes = time.split(":")
                current_time = int(hours) * 60 + int(minutes)
                if current_time <= previous_time:
                    errors.append((bus_name, name))
                    break
                previous_time = current_time
        print("Arrival time test:")
        if errors:
            for bus, stop in errors:
                print(f"bus_id line {bus}: wrong time on station {stop}")
        else:
            print("OK")

    def check_demand(self):
        transfer_stops = self.find_transfer_stops()
        errors_stops = set()
        for i in self.database:
            if i["stop_type"] == "O" and i["stop_name"] in transfer_stops:
                errors_stops.add(i["stop_name"])
        print("On demand stops test:")
        if errors_stops:
            print("Wrong stop type: {0}".format(sorted(errors_stops)))
        else:
            print("OK")


def input_database_str() -> dict:
    database = input()
    database_dict = json.loads(database)
    return database_dict


def input_database_file(file_name: str) -> dict:
    with open(file_name, "r") as json_file:
        database_dict = json.load(json_file)
    return database_dict


def main():
    # database_dict = input_database_str()
    database_dict = input_database_file("buses.json")
    database_bus_company = DataBase(database_dict)
    # database_bus_company.check_demand()
    database_bus_company.print_bus_info()


if __name__ == "__main__":
    main()
