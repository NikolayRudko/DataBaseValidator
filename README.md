# The program for checking the database of the company "Easy Rider".
_(Task from [JetBrains Academy](https://hyperskill.org "JetBrains Academy") - track: Python Core)_

We have a database in json format, the database may contain data in an incorrect format. Our task is to check the
correctness of the data. We have two documents to verify the data, the first is the **documentation**, the second is
the **diagram of the bus lines**.We enter a string (we can also use a .json file) containing the data in JSON format,
passed to standard input.

Example of input data.
```
[
    {
        "bus_id": 128,
        "stop_id": 1,
        "stop_name": "Prospekt Avenue",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": 8.12
    }
]
```

![diagram of the bus lines](img/Diagram_of_the_bus_line.jpg)
###Diagram of the bus lines
![documentation](img/Documentation.jpg)
###Documentation

The program checks:
1. ###Check that the data types match. Check that the required fields are filled in.
2. ###Check that the data format complies with the documentation.
3. ###Verify the number of stops for each line.
4. ###Make sure each bus line has exactly one starting point and one final stop.
5. ###Check that the arrival time for the upcoming stops for a given bus line is increasing.
6. ###Check that all the departure points, final stops, and transfer stations are not "On-demand".