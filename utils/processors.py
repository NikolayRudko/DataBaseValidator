import re
from collections import Counter
from functools import wraps

from utils.processor_errors import DataTypeProcessorError
from utils.processor_errors import FormatFieldsProcessorError
from utils.processor_errors import ArrivalTimeProcessorError


class DatabaseProcessor:
    def __init__(self, database):
        self._database = database
        self._type_errors = dict(bus_id=0, stop_id=0, stop_name=0, next_stop=0, stop_type=0, a_time=0)
        self._total_type_errors = 0
        self._format_errors = dict(stop_name=0, stop_type=0, a_time=0)
        self._total_format_errors = 0
        self._bus_route_info = {}
        self._arrival_time_errors = []
        self._demand_stops_errors = set()

    def _check_data_type(self) -> None:
        """
        Check input data for compliance with documentation.
        Fields 'stop_name', 'a_time' should not be empty.
        Errors are sorted and added to the type_errors dictionary. The total number of errors is also calculated.
        """
        correct_data_type = dict(bus_id=int, stop_id=int, stop_name=str, next_stop=int, stop_type=str, a_time=str)
        required_fields = ("stop_name", 'a_time')
        for stop in self._database:
            for key, value in stop.items():
                if type(value) != correct_data_type[key]:
                    self._type_errors[key] += 1
                    continue
                stop_type_pattern = r"""
                ^                           # start of string
                .                           # any of chapter
                ?                           # zero or one consecutive letter
                $                           # end of string    
                """
                stop_type_regex = re.compile(stop_type_pattern, re.VERBOSE)
                if key == "stop_type" and not stop_type_regex.match(value):
                    self._type_errors[key] += 1
                if key in required_fields and value == "":
                    self._type_errors[key] += 1
        self._total_type_errors = sum(self._type_errors.values())

    def _data_type_validator(func):
        @wraps(func)
        def wrapper(*args):
            # check type of data
            if args[0]._total_type_errors == 0:
                args[0]._check_data_type()
            ret = func(*args)
            return ret

        return wrapper

    @_data_type_validator
    def print_data_type_errors(self) -> None:
        """Prints result check_data_type()"""
        print(f"Type and required field validation: {self._total_type_errors} errors")
        for k, v in self._type_errors.items():
            print(f'{k}: {v}')

    @_data_type_validator
    def _check_format_fields(self) -> None:
        """
        Checks correctness of format fields: stop_name, stop_type, a_time.
        stop_name - must consist of two words with a space between them, the first word with a capital letter,
                    the second can be Road, Avenue, Boulevard or Street.
        stop_type - must be 'S', 'O','F' or empty string.
        a_time - must be 24 hours formate, hh:mm.
        """
        if self._total_type_errors != 0:
            raise DataTypeProcessorError("Data contain {} type errors".format(self._total_type_errors))
        stop_name_pattern = r"""
        ^                                   # start of string
        (                                   # start of first part of name 
        [A-Z]                               # first capital letter of word
        \w                                  # any letter, digit or underscore. Equivalent to [a-zA-Z0-9_]
        +                                   # one or more consecutive `\w` characters.
        \s                                  # any whitespace chapters
        )                                   # end of first part of name
        +                                   # one or more consecutive words with capital letter
        (                                   # start of second part of word
        Road|Avenue|Boulevard|Street        # one of this word is end of second part name
        )                                   # end of second part of word                    
        $                                   # end of string
        """
        stop_type_pattern = r"""
        ^                                   # start of string                       
        [SOF]                               # a single chapter of: S,O or F 
        ?                                   # zero or one consecutive letter
        $                                   # end of string
        """
        a_time_pattern = r"""
        ^                                   # start of string 
        (                                   # start of hour part
        [01]                                # first digit 1 or 0
        \d                                  # any of digit
        |                                   # or 
        2                                   # digit 2
        [0-3]                               # a single chapter of: 0,1,2 or 3 
        )                                   # end of hour part
        (:)                                 # delimiter  
        (                                   # end of minutes part
        [0-5]                               # a single chapter of: 0-5 
        \d                                  # any of digit
        )                                   # end of minutes part
        $                                   # end of string
        """
        validation_fields = {'stop_name': re.compile(stop_name_pattern, re.VERBOSE),
                             'stop_type': re.compile(stop_type_pattern, re.VERBOSE),
                             'a_time': re.compile(a_time_pattern, re.VERBOSE)}
        for stop in self._database:
            for key, value in stop.items():
                if key in validation_fields and not validation_fields[key].match(value):
                    self._format_errors[key] += 1
        self._total_format_errors = sum(self._format_errors.values())

    def _data_format_validator(func):
        @wraps(func)
        def wrapper(*args):
            # check format of data
            if args[0]._total_format_errors == 0:
                args[0]._check_format_fields()
            ret = func(*args)
            return ret

        return wrapper

    @_data_format_validator
    def print_format_fields_errors(self) -> None:
        """Prints result check_format_fields()"""
        print(f"Format validation: {self._total_format_errors} errors")
        for k, v in self._format_errors.items():
            print(f'{k}: {v}')

    @_data_format_validator
    def _calculate_stops(self) -> None:
        """
        Are processing database, then creating dict bus_route_info with information about start, final
        and intermediate stops.

        example: {"128": {[("Prospekt Avenue", "08:12")],
                        [("Elm Street", "08:19"), ...., ("Fifth Avenue", "08:25")],
                        [("Sesame Street", "08:37")]},
                ...}
        """
        if self._total_type_errors:
            raise DataTypeProcessorError("Data contain {} type errors".format(self._total_type_errors))

        self._check_format_fields()
        if self._total_format_errors:
            raise FormatFieldsProcessorError("Data contain {} format errors".format(self._total_format_errors))

        for stop in self._database:
            bus_id = stop['bus_id']
            bus = self._bus_route_info.setdefault(bus_id, dict(start=[], stops=[], finish=[]))
            stop_info = (stop["stop_name"], stop["a_time"])
            bus["stops"].append(stop_info)
            if stop["stop_type"] == "S":
                bus["start"].append(stop_info)
            elif stop["stop_type"] == "F":
                bus["finish"].append(stop_info)

    def _stops_handler(func):
        @wraps(func)
        def wrapper(*args):
            # calculate stops
            if not args[0]._bus_route_info:
                args[0]._calculate_stops()
            ret = func(*args)
            return ret

        return wrapper

    @_stops_handler
    def print_bus_info(self) -> None:
        """Prints info about buses routes."""
        print("Line names and number of stops:")
        for bus_id, stops in self._bus_route_info.items():
            print(f'bus_id: {bus_id}, stops: {len(stops["stops"])}')

    @_stops_handler
    def _find_transfer_stops(self) -> list:
        """
        Finds transfer stops. A transfer stop is a stop that is included in several routes.

        :return: List of transfer stops.
        """
        routes_stops = [stop[0] for stops in self._bus_route_info.values() for stop in stops["stops"]]
        stop_frequency = Counter(routes_stops).most_common()
        transfer_stops = sorted([stop[0] for stop in stop_frequency if stop[1] > 1])
        return transfer_stops

    @_stops_handler
    def print_stops_info(self) -> None:
        """Prints info about types of stops."""
        start_stops = set()
        finish_stops = set()
        for bus_id, stops in self._bus_route_info.items():
            if len(stops['start']) != 1 or len(stops["finish"]) != 1:
                print(f'There is no start or end stop for the line: {bus_id}.')
                break
            else:
                start_stops.update([i[0] for i in stops["start"]])
                finish_stops.update([i[0] for i in stops["finish"]])
        else:
            print(f'Start stops: {len(start_stops)} {sorted(start_stops)}')
            transfer_stops = self._find_transfer_stops()
            print(f'Transfer stops: {len(transfer_stops)} {transfer_stops}')
            print(f'Finish stops: {len(finish_stops)} {sorted(finish_stops)}')

    @_stops_handler
    def _check_arrival_time_errors(self) -> None:
        """
        Checks the time on the route, if the time of the next station is less or more than the previous one,
        the program adds an error to the time_errors list and stops checking this route
        and starts checking the next one.
        """
        for bus_id, bus in self._bus_route_info.items():
            previous_time = 0
            for stop_name, time in bus["stops"]:
                hours, minutes = time.split(":")
                current_time = int(hours) * 60 + int(minutes)
                if current_time <= previous_time:
                    self._arrival_time_errors.append((bus_id, stop_name))
                    break
                previous_time = current_time

    def _arrival_time_validator(func):
        @wraps(func)
        def wrapper(*args):
            # check arrival time
            if not args[0]._arrival_time_errors:
                args[0]._check_arrival_time_errors()
            ret = func(*args)
            return ret

        return wrapper

    @_arrival_time_validator
    def print_arrival_time_errors(self) -> None:
        """Prints result of check_time_errors()"""
        print("Arrival time test:")
        if self._arrival_time_errors:
            for bus, stop in self._arrival_time_errors:
                print(f"bus_id line {bus}: wrong time on station {stop}")
        else:
            print("OK")

    @_arrival_time_validator
    def _check_demand_errors(self) -> None:
        """
        Are checking the errors if departure points, final stops and transfer stations have attribute -O("On-demand"),
        then adding errors in set errors_stops.
        """
        if self._arrival_time_errors:
            raise ArrivalTimeProcessorError("Data contain {} arrival time errors".format(self._arrival_time_errors))
        transfer_stops = self._find_transfer_stops()
        for i in self._database:
            if i["stop_type"] == "O" and i["stop_name"] in transfer_stops:
                self._demand_stops_errors.add(i["stop_name"])

    def print_demand_errors(self) -> None:
        """
        Are printing the errors if departure points, final stops and transfer stations have attribute -O("On-demand").
        The errors are also sorted alphabetically.
        """
        if not self._demand_stops_errors:
            self._check_demand_errors()
        print("On demand stops test:")
        print("Wrong stop type: {0}".format(sorted(self._demand_stops_errors)) if self._demand_stops_errors else "OK")
