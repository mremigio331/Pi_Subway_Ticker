#!/bin/env python
from datetime import datetime
import sys
import random
import json
import time
from os.path import exists
import logging

sys.path.append("/home/pi/.local/lib/python3.9/site-packages/")

# Configure logging
logging.basicConfig(
    level="INFO",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("common")


def open_json_file(file_name, max_timeout=10):
    retries = 0
    while retries < max_timeout:
        try:
            with open(file_name, "r") as json_file:
                json_data = json.load(json_file)
            return json_data
        except Exception as e:
            retries += 1
            time.sleep(2)
    logger.error(f"Error opening up {file_name}: Max retries reached.")


def config_load_v2():
    try:
        return open_json_file("trains_config.json")
    except BaseException:
        logger.error("ERROR loading configs")


def get_log_level():
    try:
        log_level = config_load_v2()["log_level"]
        return log_level
    except Exception as e:
        logger.error(f"Error getting log level: {e}")
        return "INFO"


def random_trains():
    all_trains = [
        "A",
        "C",
        "E",
        "B",
        "D",
        "F",
        "FX",
        "M",
        "G",
        "GS",
        "J",
        "Z",
        "L",
        "N",
        "Q",
        "R",
        "W",
        "S",
        "FS",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "6X",
        "7",
        "7X",
        "T",
    ]
    train_return = []
    for x in range(6):
        train_line = str(random.choice(all_trains))
        all_trains.remove(train_line)
        train_return.append(train_line)
    return train_return


def station_check(station):
    all_stations = stations_load()
    return station in all_stations


def station_check_v2(station):
    all_stations = stations_load_v2()
    return station in list(all_stations.keys())


def build_station_element(station):
    return stations_load_v2()[station]


def stations_load():
    stations = []
    with open("data/stations.txt") as f:
        stations = [line.strip() for line in f]
    return stations


def stations_load_v2():
    try:
        return open_json_file("data/stations_config.json")
    except BaseException:
        logger.error("There was an issue opening up the train stations")
        return False


def all_data_to_json(loading, station, next_four, all_trains_data):
    data = {
        "timestamp": get_current_time(),
        "loading": loading,
        "current_station": station,
        "next_four": next_four,
        "all_trains_data": all_trains_data,
    }

    file_path = "data/export_data.json"

    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def get_current_time():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


def update_json(filename, updated_data):
    with open(filename, "w") as json_file:
        json.dump(updated_data, json_file, indent=4)


def dict_to_list_of_dicts(input_dict):
    output_list = []
    for key, value in input_dict.items():
        output_list.append({"type": key, "value": value})
    return output_list


def str_to_bool(string):
    string_lower = string.lower()
    if string_lower == "true":
        return True
    elif string_lower == "false":
        return False
    else:
        raise ValueError("Input string must be 'true' or 'false'")
