#!/bin/env python
import sys
import os
import pandas as pd
import json
import requests
from datetime import datetime, timezone
import additional_py_files.common as common
import random
try:
    from google.transit import gtfs_realtime_pb2
except:
    sys.path.append(
        '/home/pi/.local/lib/python3.9/site-packages/google/transit')
    import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict


def api_pull(line, link):
    note = 'Conducting API pull of ' + line
    common.log_add(note, 'API', 4)
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(link)
    feed.ParseFromString(response.content)
    feed = MessageToDict(feed)
    note = 'Cleaning info for ' + line
    common.log_add(note, 'API', 4)
    clean_info = subway_cleanup(feed)
    note = 'Completed cleaning up ' + line
    common.log_add(note, 'API', 4)
    return clean_info


def all_train_data():
    note = 'Starting all train data'
    common.log_add(note, 'API', 3)
    api_links = [{'line': 'ACE',
                  'link': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace'},
                 {'line': 'BDFM',
                  'link': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm'},
                 {'line': 'G',
                  'link': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g'},
                 {'line': 'JZ',
                  'link': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz'},
                 {'line': 'NQRW',
                  'link': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw'},
                 {'line': 'L',
                  'link': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l'},
                 {'line': '1234567',
                  'link': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs'},
                 {'line': 'SIR',
                  'link': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-si'}
                 ]
    all_train_info = []
    for x in api_links:
        trains = api_pull(x['line'], x['link'])
        for i in trains:
            all_train_info.append(i)
        note = 'Added information from the ' + x['line'] + ' line.'
        common.log_add(note, 'API', 4)
    data_dump(all_train_info)
    return all_train_info


def data_dump(train_info):
    data_dict = {}
    try:
        for x in train_info:
            train_id = x['id']
            data_dict.update({train_id: x})
        with open('data/subway_info.json', 'w') as json_file:
            json.dump(data_dict, json_file, indent=4)
        note = 'Successfully dump train data to a json'
        common.log_add(note, 'API', 3)
    except:
        note = 'ERROR converting train data to a json'
        common.log_add(note, 'API', 1)


def next_train_in(station, data):
    train_stops = []
    now = datetime.now()
    note = 'Time now: ' + str(now)
    common.log_add(note, 'API', 3)
    for x in data:
        try:
            for y in x['tripUpdate']['stopTimeUpdate']:
                stop = y['stop_name']
                if stop == station:
                    route = x['tripUpdate']['trip']['routeId']
                    tripID = x['tripUpdate']['trip']['tripId']
                    final_dest = x['tripUpdate']['stopTimeUpdate'][-1]['stop_name']
                    arrival_time = (datetime.fromtimestamp(
                        int(y['arrival']['time'])))
                    difference = arrival_time - now
                    arrival_time = (int(difference.total_seconds() / 60))
                    if arrival_time < 0:
                        pass
                    else:
                        route_info = {'route': route,
                                      'tripId': tripID,
                                      'final_dest': final_dest,
                                      'arrival': arrival_time,
                                      'station_info': y}
                        train_stops.append(route_info)
        except:
            pass
    train_stops.sort(key=lambda k: k['arrival'])
    note = 'Next train in complete'
    common.log_add(note, 'API', 3)
    return train_stops


def next_train_in_v2(station, data):
    station_object = common.build_station_element(station)
    train_stops = []
    now = datetime.now()
    note = 'Time now: ' + str(now)
    common.log_add(note, 'API', 3)
    for x in data:
        try:
            for y in x['tripUpdate']['stopTimeUpdate']:
                stop_id = y['stopId']
                if stop_id in station_object['stop_ids'] or str(stop_id + 'S') in station_object['stop_ids'] or str(stop_id + 'N') in station_object['stop_ids']:
                    route = x['tripUpdate']['trip']['routeId']
                    tripID = x['tripUpdate']['trip']['tripId']
                    final_dest = x['tripUpdate']['stopTimeUpdate'][-1]['stop_name']
                    arrival_time = (datetime.fromtimestamp(
                        int(y['arrival']['time'])))
                    difference = arrival_time - now
                    arrival_time = (int(difference.total_seconds() / 60))
                    if arrival_time < 0:
                        pass
                    else:
                        route_info = {'route': route,
                                      'tripId': tripID,
                                      'final_dest': final_dest,
                                      'arrival': arrival_time,
                                      'station_info': y}
                        train_stops.append(route_info)
        except:
            pass
    train_stops.sort(key=lambda k: k['arrival'])
    note = 'Next train in complete'
    common.log_add(note, 'API', 3)
    return train_stops


def random_station():
    with open('data/stations.txt') as f:
        stations = [line.strip() for line in f]
    station = random.choice(stations)
    return station


def random_station_v2():
    all_stations = common.stations_load_v2()
    while True:
        station = random.choice(list(all_stations.keys()))
        if all_stations[station]['enabled'] is True:
            return station


def subway_cleanup(train_info):
    subway_stops = pd.read_csv('data/stations.csv', index_col=None, header=0)
    subway_stops = subway_stops.set_index('stop_id')
    stop_time_update = []
    for x in train_info['entity']:
        try:
            x['tripUpdate']['stopTimeUpdate']
            stop_time_update.append(x)
        except:
            pass
    for x in stop_time_update:
        for y in x['tripUpdate']['stopTimeUpdate']:
            try:
                stop_id = y['stopId']
                stop_name = subway_stops.loc[stop_id][1]
                y.update({'stop_name': stop_name})
            except:
                pass
    return stop_time_update
