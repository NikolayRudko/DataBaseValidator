from unittest import TestCase, main
from utils.processors import DatabaseProcessor


class DatabaseProcessorTest(TestCase):
    """Test for DatabaseProcessor"""

    def test_find_bus_id_data_type_error(self):
        """Check add error in  'bus_id'"""
        wrong_id_record = [{"bus_id": "128",
                            "stop_id": 1,
                            "stop_name": "Prospekt Avenue",
                            "next_stop": 3,
                            "stop_type": "S",
                            "a_time": "8:12"
                            }]
        my_processor = DatabaseProcessor(wrong_id_record)
        my_processor.check_data_type()

        right_dict = dict(bus_id=1, stop_id=0, stop_name=0, next_stop=0, stop_type=0, a_time=0)

        self.assertDictContainsSubset(right_dict, my_processor.type_errors)
        # todo read more
        # self.assertEqual(my_processor.type_errors, my_processor.type_errors | right_dict)
        self.assertEqual(my_processor.total_type_errors, 1)

    def test_data_without_type_error(self):
        """Check 'bus_id' without errors."""
        correct_id_record = [{"bus_id": 128,
                              "stop_id": 1,
                              "stop_name": "Prospekt Avenue",
                              "next_stop": 3,
                              "stop_type": "S",
                              "a_time": "8:12"
                              }]
        my_processor = DatabaseProcessor(correct_id_record)
        my_processor.check_data_type()

        right_dict = dict(bus_id=0, stop_id=0, stop_name=0, next_stop=0, stop_type=0, a_time=0)

        self.assertDictContainsSubset(right_dict, my_processor.type_errors)
        self.assertEqual(my_processor.total_type_errors, 0)

    def test_find_stop_id_data_type_error(self):
        """Check add error in 'stop_id'"""
        wrong_id_record = [{"bus_id": 128,
                            "stop_id": "1",
                            "stop_name": "Prospekt Avenue",
                            "next_stop": 3,
                            "stop_type": "S",
                            "a_time": "8:12"
                            }]
        my_processor = DatabaseProcessor(wrong_id_record)
        my_processor.check_data_type()

        right_dict = dict(bus_id=0, stop_id=1, stop_name=0, next_stop=0, stop_type=0, a_time=0)

        self.assertDictContainsSubset(right_dict, my_processor.type_errors)
        self.assertEqual(my_processor.total_type_errors, 1)

    def test_find_stop_name_data_type_error(self):
        """Check add error in 'stop_name'"""
        wrong_id_record = [{"bus_id": 128,
                            "stop_id": 1,
                            "stop_name": 0,
                            "next_stop": 3,
                            "stop_type": "S",
                            "a_time": "8:12"
                            }]
        my_processor = DatabaseProcessor(wrong_id_record)
        my_processor.check_data_type()

        right_dict = dict(bus_id=0, stop_id=0, stop_name=1, next_stop=0, stop_type=0, a_time=0)

        self.assertDictContainsSubset(right_dict, my_processor.type_errors)
        self.assertEqual(my_processor.total_type_errors, 1)

    def test_find_next_stop_data_type_error(self):
        """Check add error in 'next_stop'"""
        wrong_id_record = [{"bus_id": 128,
                            "stop_id": 1,
                            "stop_name": "Prospekt Avenue",
                            "next_stop": "3",
                            "stop_type": "S",
                            "a_time": "8:12"
                            }]
        my_processor = DatabaseProcessor(wrong_id_record)
        my_processor.check_data_type()

        right_dict = dict(bus_id=0, stop_id=0, stop_name=0, next_stop=1, stop_type=0, a_time=0)

        self.assertDictContainsSubset(right_dict, my_processor.type_errors)
        self.assertEqual(my_processor.total_type_errors, 1)

    def test_find_stop_type_data_type_error(self):
        """Check add error in 'stop_type'"""
        wrong_id_record = [{"bus_id": 128,
                            "stop_id": 1,
                            "stop_name": "Prospekt Avenue",
                            "next_stop": 3,
                            "stop_type": 0,
                            "a_time": "8:12"
                            }]
        my_processor = DatabaseProcessor(wrong_id_record)
        my_processor.check_data_type()

        right_dict = dict(bus_id=0, stop_id=0, stop_name=0, next_stop=0, stop_type=1, a_time=0)

        self.assertDictContainsSubset(right_dict, my_processor.type_errors)
        self.assertEqual(my_processor.total_type_errors, 1)

    def test_find_a_time_data_type_error(self):
        """Check add error in 'a_time'"""
        wrong_id_record = [{"bus_id": 128,
                            "stop_id": 1,
                            "stop_name": "Prospekt Avenue",
                            "next_stop": 3,
                            "stop_type": "",
                            "a_time": 8.12
                            }]
        my_processor = DatabaseProcessor(wrong_id_record)
        my_processor.check_data_type()

        right_dict = dict(bus_id=0, stop_id=0, stop_name=0, next_stop=0, stop_type=0, a_time=1)

        self.assertDictContainsSubset(right_dict, my_processor.type_errors)
        self.assertEqual(my_processor.total_type_errors, 1)

    def test_find_stop_name_empty_field_error(self):
        """Check add error in 'stop_name'"""
        wrong_id_record = [{"bus_id": 128,
                            "stop_id": 1,
                            "stop_name": "",
                            "next_stop": 3,
                            "stop_type": "S",
                            "a_time": "8:12"
                            }]
        my_processor = DatabaseProcessor(wrong_id_record)
        my_processor.check_data_type()

        right_dict = dict(bus_id=0, stop_id=0, stop_name=1, next_stop=0, stop_type=0, a_time=0)

        self.assertDictContainsSubset(right_dict, my_processor.type_errors)
        self.assertEqual(my_processor.total_type_errors, 1)

    def test_find_a_time_empty_field_error(self):
        """Check add error in 'a_time'"""
        wrong_id_record = [{"bus_id": 128,
                            "stop_id": 1,
                            "stop_name": "Prospekt Avenue",
                            "next_stop": 3,
                            "stop_type": "",
                            "a_time": ""
                            }]
        my_processor = DatabaseProcessor(wrong_id_record)
        my_processor.check_data_type()

        right_dict = dict(bus_id=0, stop_id=0, stop_name=0, next_stop=0, stop_type=0, a_time=1)

        self.assertDictContainsSubset(right_dict, my_processor.type_errors)
        self.assertEqual(my_processor.total_type_errors, 1)

    def test_find_stop_type_format_type_error(self):
        """Check add error in 'stop_type'"""
        wrong_id_record = [{"bus_id": 128,
                            "stop_id": 1,
                            "stop_name": "Prospekt Avenue",
                            "next_stop": 3,
                            "stop_type": 0,
                            "a_time": "8:12"
                            }]
        my_processor = DatabaseProcessor(wrong_id_record)
        my_processor.check_data_type()

        right_dict = dict(bus_id=0, stop_id=0, stop_name=0, next_stop=0, stop_type=1, a_time=0)

        self.assertDictContainsSubset(right_dict, my_processor.type_errors)

    def test_find_total_type_errors(self):
        """Check total_type"""
        wrong_id_record = [
            {
                "bus_id": 128,
                "stop_id": 1,
                "stop_name": "Prospekt Avenue",
                "next_stop": 3,
                "stop_type": "S",
                "a_time": 8.12
            },
            {
                "bus_id": 128,
                "stop_id": 3,
                "stop_name": "",
                "next_stop": 5,
                "stop_type": "",
                "a_time": "08:19"
            },
            {
                "bus_id": 128,
                "stop_id": 5,
                "stop_name": "Fifth Avenue",
                "next_stop": 7,
                "stop_type": "O",
                "a_time": "08:25"
            },
            {
                "bus_id": 128,
                "stop_id": "7",
                "stop_name": "Sesame Street",
                "next_stop": 0,
                "stop_type": "F",
                "a_time": "08:37"
            },
            {
                "bus_id": "",
                "stop_id": 2,
                "stop_name": "Pilotow Street",
                "next_stop": 3,
                "stop_type": "S",
                "a_time": ""
            },
            {
                "bus_id": 256,
                "stop_id": 3,
                "stop_name": "Elm Street",
                "next_stop": 6,
                "stop_type": "",
                "a_time": "09:45"
            },
            {
                "bus_id": 256,
                "stop_id": 6,
                "stop_name": "Sunset Boulevard",
                "next_stop": 7,
                "stop_type": "",
                "a_time": "09:59"
            },
            {
                "bus_id": 256,
                "stop_id": 7,
                "stop_name": "Sesame Street",
                "next_stop": "0",
                "stop_type": "F",
                "a_time": "10:12"
            },
            {
                "bus_id": 512,
                "stop_id": 4,
                "stop_name": "Bourbon Street",
                "next_stop": 6,
                "stop_type": "S",
                "a_time": "08:13"
            },
            {
                "bus_id": "512",
                "stop_id": 6,
                "stop_name": "Sunset Boulevard",
                "next_stop": 0,
                "stop_type": 5,
                "a_time": "08:16"
            }
        ]
        my_processor = DatabaseProcessor(wrong_id_record)
        my_processor.check_data_type()

        right_dict = dict(bus_id=2, stop_id=1, stop_name=1, next_stop=1, stop_type=1, a_time=2)

        self.assertDictContainsSubset(right_dict, my_processor.type_errors)
        self.assertEqual(my_processor.total_type_errors, 8)

    def test_without_format_error(self):
        """Check without errors"""
        correct_id_record = [{"bus_id": 128,
                              "stop_id": 1,
                              "stop_name": "Prospekt Avenue",
                              "next_stop": 3,
                              "stop_type": "S",
                              "a_time": "22:00"
                              },
                             {"bus_id": 128,
                              "stop_id": 1,
                              "stop_name": "Elm Street",
                              "next_stop": 3,
                              "stop_type": "O",
                              "a_time": "00:00"
                              },
                             {"bus_id": 128,
                              "stop_id": 1,
                              "stop_name": "Sesame Street",
                              "next_stop": 3,
                              "stop_type": "F",
                              "a_time": "23:59"
                              },
                             {"bus_id": 128,
                              "stop_id": 1,
                              "stop_name": "Sunset Boulevard",
                              "next_stop": 3,
                              "stop_type": "",
                              "a_time": "08:12"
                              }]
        my_processor = DatabaseProcessor(correct_id_record)
        my_processor.check_format_fields()

        correct_error_dict = dict(stop_name=0, stop_type=0, a_time=0)

        self.assertDictContainsSubset(correct_error_dict, my_processor.format_errors)
        self.assertEqual(my_processor.total_format_errors, 0)

    def test_find_a_time_format_error(self):
        """Check a_time without errors"""
        correct_id_record = [{"bus_id": 128,
                              "stop_id": 1,
                              "stop_name": "Prospekt Avenue",
                              "next_stop": 3,
                              "stop_type": "S",
                              "a_time": "24:00"
                              },
                             {"bus_id": 146,
                              "stop_id": 4,
                              "stop_name": "Sunset Boulevard",
                              "next_stop": 9,
                              "stop_type": "",
                              "a_time": "00:72"
                              },
                             {"bus_id": 193,
                              "stop_id": 1,
                              "stop_name": "Prospekt Avenue",
                              "next_stop": 3,
                              "stop_type": "S",
                              "a_time": "32:00"
                              },
                             {"bus_id": 34,
                              "stop_id": 1,
                              "stop_name": "Elm Street",
                              "next_stop": 3,
                              "stop_type": "O",
                              "a_time": "0:00"
                              },
                             {"bus_id": 92,
                              "stop_id": 1,
                              "stop_name": "Sesame Street",
                              "next_stop": 3,
                              "stop_type": "F",
                              "a_time": "23.59"
                              },
                             {"bus_id": 18,
                              "stop_id": 1,
                              "stop_name": "Sunset Boulevard",
                              "next_stop": 3,
                              "stop_type": "",
                              "a_time": "08/12"
                              },
                             {"bus_id": 1835,
                              "stop_id": 1,
                              "stop_name": "Sesame Street",
                              "next_stop": 3,
                              "stop_type": "F",
                              "a_time": "25.59"
                              }
                             ]
        my_processor = DatabaseProcessor(correct_id_record)
        my_processor.check_format_fields()

        correct_error_dict = dict(stop_name=0, stop_type=0, a_time=7)

        self.assertDictContainsSubset(correct_error_dict, my_processor.format_errors)
        self.assertEqual(my_processor.total_format_errors, 7)

    def test_find_stop_name_format_error(self):
        """Check without errors"""
        correct_id_record = [{"bus_id": 128,
                              "stop_id": 1,
                              "stop_name": "prospekt Avenue",
                              "next_stop": 3,
                              "stop_type": "S",
                              "a_time": "22:00"
                              },
                             {"bus_id": 128,
                              "stop_id": 1,
                              "stop_name": "Elm St.",
                              "next_stop": 3,
                              "stop_type": "O",
                              "a_time": "00:00"
                              },
                             {"bus_id": 128,
                              "stop_id": 1,
                              "stop_name": "SesameStreet",
                              "next_stop": 3,
                              "stop_type": "F",
                              "a_time": "23:59"
                              },
                             {"bus_id": 128,
                              "stop_id": 1,
                              "stop_name": "Boulevard",
                              "next_stop": 3,
                              "stop_type": "",
                              "a_time": "08:12"
                              }]
        my_processor = DatabaseProcessor(correct_id_record)
        my_processor.check_format_fields()

        correct_error_dict = dict(stop_name=4, stop_type=0, a_time=0)

        self.assertDictContainsSubset(correct_error_dict, my_processor.format_errors)
        self.assertEqual(my_processor.total_format_errors, 4)

    def test_find_stop_type_format_error(self):
        """Check without errors"""
        correct_id_record = [{"bus_id": 128,
                              "stop_id": 1,
                              "stop_name": "Prospekt Avenue",
                              "next_stop": 3,
                              "stop_type": "A",
                              "a_time": "22:00"
                              },
                             {"bus_id": 128,
                              "stop_id": 1,
                              "stop_name": "Elm Street",
                              "next_stop": 3,
                              "stop_type": "1",
                              "a_time": "00:00"
                              },
                             {"bus_id": 128,
                              "stop_id": 1,
                              "stop_name": "Sesame Street",
                              "next_stop": 3,
                              "stop_type": "f",
                              "a_time": "23:59"
                              },
                             {"bus_id": 128,
                              "stop_id": 1,
                              "stop_name": "Sunset Boulevard",
                              "next_stop": 3,
                              "stop_type": "OO",
                              "a_time": "08:12"
                              }]
        my_processor = DatabaseProcessor(correct_id_record)
        my_processor.check_format_fields()

        correct_error_dict = dict(stop_name=0, stop_type=4, a_time=0)

        self.assertDictContainsSubset(correct_error_dict, my_processor.format_errors)
        self.assertEqual(my_processor.total_format_errors, 4)

    def test_find_format_error(self):
        """Check without errors"""
        correct_id_record = [
            {
                "bus_id": 128,
                "stop_id": 1,
                "stop_name": "Prospekt Av.",
                "next_stop": 3,
                "stop_type": "S",
                "a_time": "08:12"
            },
            {
                "bus_id": 128,
                "stop_id": 3,
                "stop_name": "Elm Street",
                "next_stop": 5,
                "stop_type": "",
                "a_time": "8:19"
            },
            {
                "bus_id": 128,
                "stop_id": 5,
                "stop_name": "Fifth Avenue",
                "next_stop": 7,
                "stop_type": "OO",
                "a_time": "08:25"
            },
            {
                "bus_id": 128,
                "stop_id": 7,
                "stop_name": "Sesame Street",
                "next_stop": 0,
                "stop_type": "F",
                "a_time": "08:77"
            },
            {
                "bus_id": 256,
                "stop_id": 2,
                "stop_name": "Pilotow Street",
                "next_stop": 3,
                "stop_type": "S",
                "a_time": "09:20"
            },
            {
                "bus_id": 256,
                "stop_id": 3,
                "stop_name": "Elm",
                "next_stop": 6,
                "stop_type": "",
                "a_time": "09:45"
            },
            {
                "bus_id": 256,
                "stop_id": 6,
                "stop_name": "Sunset Boulevard",
                "next_stop": 7,
                "stop_type": "A",
                "a_time": "09:59"
            },
            {
                "bus_id": 256,
                "stop_id": 7,
                "stop_name": "Sesame Street",
                "next_stop": 0,
                "stop_type": "F",
                "a_time": "10.12"
            },
            {
                "bus_id": 512,
                "stop_id": 4,
                "stop_name": "bourbon street",
                "next_stop": 6,
                "stop_type": "S",
                "a_time": "38:13"
            },
            {
                "bus_id": 512,
                "stop_id": 6,
                "stop_name": "Sunset Boulevard",
                "next_stop": 0,
                "stop_type": "F",
                "a_time": "08:16"
            }
        ]
        my_processor = DatabaseProcessor(correct_id_record)
        my_processor.check_format_fields()

        correct_error_dict = dict(stop_name=3, stop_type=2, a_time=4)

        self.assertDictContainsSubset(correct_error_dict, my_processor.format_errors)
        self.assertEqual(my_processor.total_format_errors, 9)


if __name__ == "__main__":
    main()