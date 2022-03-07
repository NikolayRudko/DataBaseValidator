from unittest import TestCase, main
from utils.processors import DatabaseProcessor
from utils.processor_errors import DataTypeProcessorError, ArrivalTimeProcessorError
from utils.processor_errors import FormatFieldsProcessorError
from utils.processor_handler import input_database_file


class DatabaseProcessorTest(TestCase):
    """Test for DatabaseProcessor"""
    DATA_FIND_BUS_TYPE_ERRORS = input_database_file("test_data/data_find_bus_type_errors.json")
    DATA_WITHOUT_TYPE_ERRORS = input_database_file("test_data/data_without_type_errors.json")
    DATA_WITHOUT_FORMAT_ERRORS = input_database_file("test_data/data_without_format_errors.json")
    DATA_FIND_A_TIME_FORMAT_ERRORS = input_database_file("test_data/data_find_a_time_format_errors.json")
    DATA_FIND_STOP_NAME_FORMAT_ERRORS = input_database_file("test_data/data_find_stop_name_format_errors.json")
    DATA_FIND_STOP_TYPE_FORMAT_ERRORS = input_database_file("test_data/data_find_stop_type_format_errors.json")
    DATA_FIND_FORMAT_ERRORS = input_database_file("test_data/data_find_format_errors.json")
    DATA_FIND_FORMAT_ERRORS_WITH_DATA_TYPE_PROCESSOR_ERRORS = input_database_file(
        "test_data/data_find_format_error_with_data_type_processor_errors.json")
    DATA_CALCULATE_STOPS = input_database_file("test_data/data_calculate_stops.json")
    DATA_CALCULATE_STOPS_WITH_DATA_TYPE_PROCESSOR_ERROR_BROKEN_BUS_ID = input_database_file(
        "test_data/data_calculate_stops_with_data_type_processor_error_broken_bus_id.json")
    DATA_CALCULATE_STOPS_WITH_FORMAT_FIELDS_PROCESSOR_ERROR_STOP_NAME = input_database_file(
        "test_data/data_calculate_stops_with_format_fields_processor_error_stop_name.json")
    DATA_FIND_TRANSFER_STOPS = input_database_file("test_data/data_find_transfer_stops.json")
    DATA_FIND_TIME_ERRORS_WITH_CORRECT_DATA = input_database_file(
        "test_data/data_find_time_errors_with_correct_data.json")
    DATA_CHECK_ARRIVAL_TIME_ERRORS_WITH_DATA_TYPE_PROCESSOR_ERROR_BROKEN_BUS_ID = input_database_file(
        "test_data/data_check_arrival_time_errors_with_data_type_processor_error_broken_bus_id.json")
    DATA_CHECK_ARRIVAL_TIME_ERRORS_WITH_FORMAT_FIELDS_PROCESSOR_ERROR_STOP_NAME = input_database_file(
        "test_data/data_check_arrival_time_errors_with_format_fields_processor_error_stop_name.json")
    DATA_FIND_TIME_ERRORS = input_database_file("test_data/data_find_time_errors.json")
    DATA_FIND_DEMAND_ERRORS_WITH_CORRECT_DATA = input_database_file(
        "test_data/data_find_demand_errors_with_correct_data.json")
    DATA_FIND_DEMAND_ERRORS = input_database_file("test_data/data_find_demand_errors.json")
    DATA_CHECK_DEMAND_ERRORS_WITH_DATA_TYPE_PROCESSOR_ERROR_BROKEN_BUS_ID = input_database_file(
        "test_data/data_check_demand_errors_with_data_type_processor_error_broken_bus_id.json")
    DATA_CHECK_DEMAND_ERRORS_WITH_FORMAT_FIELDS_PROCESSOR_ERROR_STOP_NAME = input_database_file(
        "test_data/data_check_demand_errors_with_format_fields_processor_error_stop_name.json")
    DATA_CHECK_DEMAND_ERRORS_WITH_ARRIVAL_TIME_PROCESSOR_ERROR = input_database_file(
        "test_data/data_check_demand_errors_with_arrival_time_processor_error.json")

    def test_find_bus_type_errors(self):
        """Check add error in  'bus_id'"""
        my_processor = DatabaseProcessor(self.DATA_FIND_BUS_TYPE_ERRORS)
        my_processor._check_data_type()

        right_dict = dict(bus_id=1, stop_id=1, stop_name=2, next_stop=1, stop_type=2, a_time=2)

        self.assertDictContainsSubset(right_dict, my_processor._type_errors)

        # self.assertEqual(my_processor.type_errors, my_processor.type_errors | right_dict)
        self.assertEqual(my_processor._total_type_errors, 9)

    def test_data_without_type_error(self):
        """Check 'bus_id' without errors."""
        my_processor = DatabaseProcessor(self.DATA_WITHOUT_TYPE_ERRORS)
        my_processor._check_data_type()

        right_dict = dict(bus_id=0, stop_id=0, stop_name=0, next_stop=0, stop_type=0, a_time=0)

        self.assertDictContainsSubset(right_dict, my_processor._type_errors)
        self.assertEqual(my_processor._total_type_errors, 0)

    def test_without_format_errors(self):
        """Check without errors"""
        my_processor = DatabaseProcessor(self.DATA_WITHOUT_FORMAT_ERRORS)
        my_processor._check_format_fields()

        correct_error_dict = dict(stop_name=0, stop_type=0, a_time=0)

        self.assertDictContainsSubset(correct_error_dict, my_processor._format_errors)
        self.assertEqual(my_processor._total_format_errors, 0)

    def test_find_a_time_format_errors(self):
        """Check a_time without errors"""
        my_processor = DatabaseProcessor(self.DATA_FIND_A_TIME_FORMAT_ERRORS)
        my_processor._check_format_fields()

        correct_error_dict = dict(stop_name=0, stop_type=0, a_time=7)

        self.assertDictContainsSubset(correct_error_dict, my_processor._format_errors)
        self.assertEqual(my_processor._total_format_errors, 7)

    def test_find_stop_name_format_errors(self):
        """Check without errors"""
        my_processor = DatabaseProcessor(self.DATA_FIND_STOP_NAME_FORMAT_ERRORS)
        my_processor._check_format_fields()

        correct_error_dict = dict(stop_name=4, stop_type=0, a_time=0)

        self.assertDictContainsSubset(correct_error_dict, my_processor._format_errors)
        self.assertEqual(my_processor._total_format_errors, 4)

    def test_find_stop_type_format_errors(self):
        """Check errors in stop_type"""
        my_processor = DatabaseProcessor(self.DATA_FIND_STOP_TYPE_FORMAT_ERRORS)
        my_processor._check_format_fields()

        correct_error_dict = dict(stop_name=0, stop_type=3, a_time=0)

        self.assertDictContainsSubset(correct_error_dict, my_processor._format_errors)
        self.assertEqual(my_processor._total_format_errors, 3)

    def test_find_format_errors(self):
        """Check complex errors"""
        my_processor = DatabaseProcessor(self.DATA_FIND_FORMAT_ERRORS)
        my_processor._check_format_fields()

        correct_error_dict = dict(stop_name=3, stop_type=1, a_time=4)

        self.assertDictContainsSubset(correct_error_dict, my_processor._format_errors)
        self.assertEqual(my_processor._total_format_errors, 8)

    def test_find_format_errors_with_data_type_processor_errors(self):
        """Checking DatabaseProcessor.calculate_stops with broken type 'bus_id' """
        my_processor = DatabaseProcessor(self.DATA_FIND_FORMAT_ERRORS_WITH_DATA_TYPE_PROCESSOR_ERRORS)

        self.assertRaises(DataTypeProcessorError, my_processor._check_format_fields)

    def test_calculate_stops(self):
        """Checking creating _bus_route_info"""
        my_processor = DatabaseProcessor(self.DATA_CALCULATE_STOPS)
        correct_bus_route_info = {
            128: {
                'start': [
                    ("Prospekt Avenue", "08:12")
                ],
                'stops': [
                    ("Prospekt Avenue", "08:12"),
                    ("Elm Street", "08:19"),
                    ("Fifth Avenue", "08:25"),
                    ("Sesame Street", "08:37")
                ],
                'finish': [
                    ("Sesame Street", "08:37")
                ]
            },
            512: {
                'start': [
                    ("Bourbon Street", "08:13")
                ],
                'stops': [
                    ("Bourbon Street", "08:13"), ("Sunset Boulevard", "08:16")
                ],
                'finish': [
                    ("Sunset Boulevard", "08:16")
                ]
            }

        }

        my_processor._calculate_stops()

        self.assertDictContainsSubset(correct_bus_route_info, my_processor._bus_route_info)

    def test_calculate_stops_with_data_type_processor_error_broken_bus_id(self):
        """Checking DatabaseProcessor._calculate_stops with broken type 'bus_id' """
        my_processor = DatabaseProcessor(self.DATA_CALCULATE_STOPS_WITH_DATA_TYPE_PROCESSOR_ERROR_BROKEN_BUS_ID)

        self.assertRaises(DataTypeProcessorError, my_processor._calculate_stops)

    def test_calculate_stops_with_format_fields_processor_error_stop_name(self):
        """Checking DatabaseProcessor._calculate_stops with broken format field 'stop_name' """
        my_processor = DatabaseProcessor(self.DATA_CALCULATE_STOPS_WITH_FORMAT_FIELDS_PROCESSOR_ERROR_STOP_NAME)

        self.assertRaises(FormatFieldsProcessorError, my_processor._calculate_stops)

    def test_find_transfer_stops(self):
        """Check converting database to list transfer stops."""
        correct_transfer_list = ["Elm Street", "Sesame Street", "Sunset Boulevard"]
        my_processor = DatabaseProcessor(self.DATA_FIND_TRANSFER_STOPS)
        my_processor._calculate_stops()
        answer = my_processor._find_transfer_stops()

        self.assertListEqual(answer, correct_transfer_list)

    def test_find_time_errors_with_correct_data(self):
        """Check DatabaseProcessor._arrival_time_errors with incorrect test_data."""
        my_processor = DatabaseProcessor(self.DATA_FIND_TIME_ERRORS_WITH_CORRECT_DATA)
        my_processor._check_arrival_time_errors()

        self.assertFalse(my_processor._arrival_time_errors)

    def test_check_arrival_time_errors_with_data_type_processor_error_broken_bus_id(self):
        """Checking DatabaseProcessor._check_arrival_time_errors with broken type 'bus_id' """
        my_processor = DatabaseProcessor(
            self.DATA_CHECK_ARRIVAL_TIME_ERRORS_WITH_DATA_TYPE_PROCESSOR_ERROR_BROKEN_BUS_ID)

        self.assertRaises(DataTypeProcessorError, my_processor._check_arrival_time_errors)

    def test_check_arrival_time_errors_with_format_fields_processor_error_stop_name(self):
        """Checking DatabaseProcessor._check_arrival_time_errors with broken format field 'stop_name' """
        my_processor = DatabaseProcessor(
            self.DATA_CHECK_ARRIVAL_TIME_ERRORS_WITH_FORMAT_FIELDS_PROCESSOR_ERROR_STOP_NAME)

        self.assertRaises(FormatFieldsProcessorError, my_processor._check_arrival_time_errors)

    def test_find_time_errors(self):
        """Check DatabaseProcessor._arrival_time_errors with wrong test_data."""
        my_processor = DatabaseProcessor(self.DATA_FIND_TIME_ERRORS)
        my_processor._check_arrival_time_errors()
        correct_error_list = [(128, "Fifth Avenue"), (256, "Sunset Boulevard")]

        self.assertListEqual(my_processor._arrival_time_errors, correct_error_list)

    def test_find_demand_errors_with_correct_data(self):
        """Check DatabaseProcessor._check_demand_errors() with correct test_data."""
        my_processor = DatabaseProcessor(self.DATA_FIND_DEMAND_ERRORS_WITH_CORRECT_DATA)
        my_processor._check_demand_errors()

        self.assertFalse(my_processor._demand_stops_errors)

    def test_find_demand_errors(self):
        """Check DatabaseProcessor._check_demand_errors() with wrong test_data."""
        my_processor = DatabaseProcessor(self.DATA_FIND_DEMAND_ERRORS)
        my_processor._check_demand_errors()
        correct_error_list = {'Sunset Boulevard', 'Elm Street'}

        self.assertSetEqual(my_processor._demand_stops_errors, correct_error_list)

    def test_check_demand_errors_with_data_type_processor_error_broken_bus_id(self):
        """Checking DatabaseProcessor._check_demand_error with broken type 'bus_id'."""
        my_processor = DatabaseProcessor(self.DATA_CHECK_DEMAND_ERRORS_WITH_DATA_TYPE_PROCESSOR_ERROR_BROKEN_BUS_ID)

        self.assertRaises(DataTypeProcessorError, my_processor._check_demand_errors)

    def test_check_demand_errors_with_format_fields_processor_error_stop_name(self):
        """Checking DatabaseProcessor._check_demand_error with broken format field 'stop_name'."""
        my_processor = DatabaseProcessor(self.DATA_CHECK_DEMAND_ERRORS_WITH_FORMAT_FIELDS_PROCESSOR_ERROR_STOP_NAME)

        self.assertRaises(FormatFieldsProcessorError, my_processor._check_demand_errors)

    def test_check_demand_errors_with_arrival_time_processor_error(self):
        """Checking DatabaseProcessor._check_demand_error with broken arrival time."""
        my_processor = DatabaseProcessor(self.DATA_CHECK_DEMAND_ERRORS_WITH_ARRIVAL_TIME_PROCESSOR_ERROR)

        self.assertRaises(ArrivalTimeProcessorError, my_processor._check_demand_errors)


if __name__ == "__main__":
    main()
