import json
import re


class DataBase:
    TIME_PATTERN = re.compile(r"""^([01]\d|2[0-4])                  # hours format 
                                            (:)                     # delimier                
                                            ([0-5]\d)$              # minutes format
                                            """, flags=re.VERBOSE)
    STOP_TYPE_PATTERN = re.compile(r"^[S|O|F]{,1}$")
    STOP_NAME_PATTERN = re.compile(r"^([A-Z]\w+ )+(Road|Avenue|Boulevard|Street)$")

    def __init__(self, database):
        self.database = database
        self.errors = {
            "bus_id": 0,
            "stop_id": 0,
            "stop_name": 0,
            "next_stop": 0,
            "stop_type": 0,
            "a_time": 0
        }
        self.total_errors = 0
        self.bus_info = {}

    def check_data(self):
        for i in self.database:
            if not isinstance(i['bus_id'], int):
                self.errors['bus_id'] += 1
            if not isinstance(i["stop_id"], int):
                self.errors["stop_id"] += 1
            if not self.check_field(i["stop_name"], self.STOP_NAME_PATTERN):
                self.errors["stop_name"] += 1
            if not isinstance(i["next_stop"], int):
                self.errors["next_stop"] += 1
            if not self.check_field(i["stop_type"], self.STOP_TYPE_PATTERN):
                self.errors["stop_type"] += 1
            if not self.check_field(i["a_time"], self.TIME_PATTERN):
                self.errors["a_time"] += 1
        self.calculate_total_errors()

    def check_field(self, field, field_pattern) -> bool:
        return isinstance(field, str) and field_pattern.match(field)

    def calculate_total_errors(self):
        self.total_errors = 0
        for err in self.errors.values():
            self.total_errors += err

    def print_errors(self):
        self.check_data()
        print(f"Format validation: {self.total_errors} errors")
        for k, v in self.errors.items():
            if k in ['stop_name', 'stop_type', 'a_time']:
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
    database_dict = input_database_str()
    # database_dict = input_database_file("example1.json")
    database_bus_company = DataBase(database_dict)
    database_bus_company.check_demand()


if __name__ == "__main__":
    main()
