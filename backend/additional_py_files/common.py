#!/bin/env python
from datetime import datetime
import sys
import random
import json
import time
from os.path import exists

sys.path.append("/home/pi/.local/lib/python3.9/site-packages/")


def open_json_file(file_name, max_timeout=3):
    retries = 0
    while retries < max_timeout:
        try:
            with open(file_name, "r") as json_file:
                json_data = json.load(json_file)
            return json_data
        except Exception as e:
            retries += 1
            time.sleep(2)
    note = f"Error opening up {file_name}: Max retries reached."
    log_add(note, "Common", 1)


def config_load_v2():
    try:
        return open_json_file("trains_config.json")
    except BaseException:
        note = "ERROR loading configs"
        log_add(note, "Common", 1)


def log_add(note, log_from, level):
    logging_level = log_level()  # identifies what the log level is in the config file
    lines = config_load_v2()
    create_log_file = False
    log_file = lines["log_file_name"]
    error_logs = lines["log_error_file_name"]
    create_log_file = lines["create_log_file"]
    if create_log_file == "True":
        create_log_file = True
    else:
        create_log_file = False
    error_logs = error_logs
    log_file_exists = exists(log_file)
    error_log_file_exists = exists(error_logs)
    if create_log_file is True:
        if (
            log_file_exists is False
        ):  # if a log file does not exist a new file will be created
            with open(log_file, "w") as f:
                now = datetime.now().isoformat()[:-3] + "Z"
                full_note = (
                    "[" + log_from + " Log " + now + "] " + "New Log File Created"
                )
                full_note = str(full_note)
                f.write(full_note + "\n")
                f.close()
            print(full_note)
        if (
            error_log_file_exists is False
        ):  # if a log file does not exist a new file will be created
            with open(error_logs, "w") as f:
                now = datetime.now().isoformat()[:-3] + "Z"
                full_note = (
                    "[" + log_from + " Log " + now + "] " + "New Error File Created"
                )
                full_note = str(full_note)
                f.write(full_note + "\n")
                f.close()
            print(full_note)
    # will log information if level is smaller or equal to the config log level
    if int(level) <= int(logging_level):
        now = datetime.now().isoformat()[:-3] + "Z"
        full_note = "[" + log_from + " Log " + now + "] " + note
        full_note = str(full_note)
        if create_log_file is True:
            with open(log_file, "a") as f:
                f.write(full_note + "\n")
                f.close()
        print(full_note)
    if int(level) == 1:
        now = datetime.now().isoformat()[:-3] + "Z"
        full_note = "[" + log_from + " Log " + now + "] " + note
        full_note = str(full_note)
        if create_log_file is True:
            with open(error_logs, "a") as f:
                f.write(full_note + "\n")
                f.close()
        print(full_note)


def log_level():
    lines = config_load_v2()
    log_levels = ["VERBOSE", "LOG+", "INFO", "ERROR", "OFF"]
    log_level = lines["log_level"]
    if log_level in log_levels:
        if log_level == "VERBOSE":
            return 4
        elif log_level == "LOG+":
            return 3
        elif log_level == "INFO":
            return 2
        elif log_level == "ERROR":
            return 1
        elif log_level == "OFF":
            return 0
    else:
        with open(lines["log_file"], "a") as f:
            now = datetime.utcnow().isoformat()[:-3] + "Z"
            full_note = (
                "[System Log "
                + now
                + "] Config file contains the following errors: ['Invalid Log Level Input']"
            )

            full_note = str(full_note)
            f.write(full_note + "\n")
            f.close()
            print(full_note)
            sys.exit()


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
    if station in all_stations:
        return True
    else:
        return False


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
        note = "There was an issue opening up the train stations"
        log_add(note, "Common", 1)
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
    # Convert the string to lowercase for case-insensitive comparison
    string_lower = string.lower()

    # Check if the string is "true" or "false" and return the corresponding
    # boolean value
    if string_lower == "true":
        return True
    elif string_lower == "false":
        return False
    else:
        raise ValueError("Input string must be 'true' or 'false'")
