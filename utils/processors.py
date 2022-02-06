import re


class DatabaseProcessor:
    def __init__(self, database):
        self.database = database
        self.format_errors = dict(stop_name=0, stop_type=0, a_time=0)
        self.total_format_errors = 0
        self.type_errors = dict(bus_id=0, stop_id=0, stop_name=0, next_stop=0, stop_type=0, a_time=0)
        self.total_type_errors = 0
        self.bus_route_info = {}
        self.time_errors = []
        self.errors_stops = set()

    def check_data_type(self) -> None:
        correct_data_type = dict(bus_id=int, stop_id=int, stop_name=str, next_stop=int, stop_type=str, a_time=str)
        required_fields = ["stop_name", 'a_time']
        for stop in self.database:
            for key, value in stop.items():
                if type(value) != correct_data_type[key]:
                    self.type_errors[key] += 1
                    continue
                if key == "stop_type" and not re.match(r"^.?$", value):
                    self.type_errors[key] += 1
                if key in required_fields and value == "":
                    self.type_errors[key] += 1
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

    def calculate_stops(self) -> None:
        """
        Are processing database, then creating dict bus_route_info with information about start, final
        and intermediate stops.

        example: {"128": {[("Prospekt Avenue", "08:12")],
                        [("Elm Street", "08:19"), ...., ("Fifth Avenue", "08:25")],
                        [("Sesame Street", "08:37")]},
                ...}
        """
        for i in self.database:
            bus_id = i['bus_id']
            if bus_id not in self.bus_route_info:
                self.bus_route_info[bus_id] = dict(start=[], stops=[], finish=[])
            stop_info = (i["stop_name"], i["a_time"])
            self.bus_route_info[bus_id]["stops"].append(stop_info)
            if i["stop_type"] == "S":
                self.bus_route_info[bus_id]["start"].append(stop_info)
            elif i["stop_type"] == "F":
                self.bus_route_info[bus_id]["finish"].append(stop_info)

    def print_bus_info(self) -> None:
        self.calculate_stops()
        print("Line names and number of stops:")
        for bus_id, stops in self.bus_route_info.items():
            print(f'bus_id: {bus_id}, stops: {len(stops["stops"])}')

    def find_transfer_stops(self) -> list:
        """
        Finds transfer stops. A transfer stop is a stop that is included in several routes.

        :return: List of transfer stops.
        """
        routes_stops = []
        for stops in self.bus_route_info.values():
            temp = []
            for stop in stops["stops"]:
                temp.append(stop[0])
            routes_stops.append(temp)
        # If the bus_route_info dictionary is empty or only one route exists.
        if len(routes_stops) <= 1:
            return []
        # todo find short solution, maybe the Counter will be better
        transfer_stops = set()
        for i in range(0, len(routes_stops) - 1):
            for j in range(i + 1, len(routes_stops)):
                transfer_stops.update(set(routes_stops[i]) & set(routes_stops[j]))
        return sorted(transfer_stops)

    def print_stops_info(self) -> None:
        self.calculate_stops()
        start_stops = set()
        finish_stops = set()
        for bus_id, stops in self.bus_route_info.items():
            if len(stops['start']) != 1 or len(stops["finish"]) != 1:
                print(f'There is no start or end stop for the line: {bus_id}.')
                break
            else:
                start_stops.update([i[0] for i in stops["start"]])
                finish_stops.update([i[0] for i in stops["finish"]])
        else:
            print(f'Start stops: {len(start_stops)} {sorted(start_stops)}')
            transfer_stops = self.find_transfer_stops()
            print(f'Transfer stops: {len(transfer_stops)} {transfer_stops}')
            print(f'Finish stops: {len(finish_stops)} {sorted(finish_stops)}')

    def check_time_errors(self) -> None:
        """
        Checks the time on the route, if the time of the next station is less or more than the previous one,
        the program adds an error to the time_errors list and stops checking this route
        and starts checking the next one.
        """
        self.calculate_stops()
        for bus_name, bus in self.bus_route_info.items():
            previous_time = 0
            for name, time in bus["stops"]:
                # todo use datetime module for it
                hours, minutes = time.split(":")
                current_time = int(hours) * 60 + int(minutes)
                if current_time <= previous_time:
                    self.time_errors.append((bus_name, name))
                    break
                previous_time = current_time

    def print_time_errors(self) -> None:
        self.check_time_errors()
        print("Arrival time test:")
        if self.time_errors:
            for bus, stop in self.time_errors:
                print(f"bus_id line {bus}: wrong time on station {stop}")
        else:
            print("OK")

    def check_demand_errors(self) -> None:
        """
        Are checking the errors if departure points, final stops and transfer stations have attribute -O("On-demand"),
        then adding errors in set errors_stops.
        """
        self.calculate_stops()
        transfer_stops = self.find_transfer_stops()
        for i in self.database:
            if i["stop_type"] == "O" and i["stop_name"] in transfer_stops:
                self.errors_stops.add(i["stop_name"])

    def print_demand_errors(self) -> None:
        """
        Are printing the errors if departure points, final stops and transfer stations have attribute -O("On-demand").
        The errors are also sorted alphabetically.
        """
        self.check_demand_errors()
        print("On demand stops test:")
        if self.errors_stops:
            print("Wrong stop type: {0}".format(sorted(self.errors_stops)))
        else:
            print("OK")
