#!/bin/env python
from datetime import datetime
import sys
import random
from os.path import exists
sys.path.append('/home/pi/.local/lib/python3.9/site-packages/')

def api_keys_check():
    try:
        api_key = config_return('api_key')
        return True
    except:
        return False

def config_load():
    try:
        configs = []
        with open('trains.conf') as f:
            general_configs = [line.strip() for line in f]
        for x in general_configs:
            configs.append(x)
        return configs
    except:
        note = 'ERROR loading configs'
        log_add(note,'Common',1)

def config_return(conf):
    configs = config_load()
    for x in configs:
        if conf in x:
            element = x.split(' = ')[1]
            return str(element)

def log_add(note,log_from,level):
    logging_level = log_level()  # identifies what the log level is in the config file
    lines = config_load()
    create_log_file = False
    for x in lines:
        if 'log_file_name' in x:
            log_file = x.split('=')[1].strip()
        if 'log_error_file_name' in x:
            error_logs = x.split('=')[1].strip()
        if 'create_log_file' in x:
            create_log_file = x.split('=')[1].strip()
            if create_log_file == 'True':
                create_log_file = True
            else:
                create_log_file = False
    error_logs = error_logs
    log_file_exists = exists(log_file)
    error_log_file_exists = exists(error_logs)
    if create_log_file is True:
        if log_file_exists is False:  # if a log file does not exist a new file will be created
            with open(log_file, 'w') as f:
                now = datetime.now().isoformat()[:-3] + 'Z'
                full_note = '[' + log_from + ' Log ' + now + '] ' + 'New Log File Created'
                full_note = str(full_note)
                f.write(full_note + '\n')
                f.close()
            print(full_note)
        if error_log_file_exists is False:  # if a log file does not exist a new file will be created
            with open(error_logs, 'w') as f:
                now = datetime.now().isoformat()[:-3] + 'Z'
                full_note = '[' + log_from + ' Log ' + now + '] ' + 'New Error File Created'
                full_note = str(full_note)
                f.write(full_note + '\n')
                f.close()
            print(full_note)
    if int(level) <= int(logging_level):  # will log information if level is smaller or equal to the config log level
        now = datetime.now().isoformat()[:-3] + 'Z'
        full_note = '[' + log_from + ' Log ' + now + '] ' + note
        full_note = str(full_note)
        if create_log_file is True: 
            with open(log_file, 'a') as f:
                f.write(full_note + '\n')
                f.close()
        print(full_note)
    if int(level) == 1:
        now = datetime.now().isoformat()[:-3] + 'Z'
        full_note = '[' + log_from + ' Log ' + now + '] ' + note
        full_note = str(full_note)
        if create_log_file is True: 
            with open(error_logs, 'a') as f: 
                f.write(full_note + '\n')
                f.close()
        print(full_note)
    
def log_level():
    lines = config_load()
    log_levels = ['VERBOSE', 'LOG+', 'INFO', 'ERROR', 'OFF']
    for x in lines:
        if 'log_level' in x:
            log_level = x.split(' = ')[1]
        if 'log_file_name' in x:
            log_file = x.split('=')[1].strip()
    if log_level in log_levels:
        if log_level == 'VERBOSE':
            return 4
        elif log_level == 'LOG+':
            return 3
        elif log_level == 'INFO':
            return 2
        elif log_level == 'ERROR':
            return 1
        elif log_level == 'OFF':
            return 0
    else:
        with open(log_file, 'a') as f:
            now = datetime.utcnow().isoformat()[:-3] + 'Z'
            full_note = ('[System Log ' +
                         now +
                         "] Config file contains the following errors: ['Invalid Log Level Input']")

            full_note = str(full_note)
            f.write(full_note + '\n')
            f.close()
            print(full_note)
            sys.exit()

def random_trains():
    all_trains =  ['A','C','E',
                   'B','D','F','FX','M',
                   'G','GS',
                   'J','Z',
                   'L',
                   'N','Q','R','W',
                   'S','FS',
                   '1','2','3',
                   '4','5','6','6X',
                   '7','7X',
                   'T']
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
           
def stations_load():
    stations = []
    with open('data/stations.txt') as f:
        stations = [line.strip() for line in f]
    return stations