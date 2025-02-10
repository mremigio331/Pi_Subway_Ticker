#!/bin/env python
import sys
import os
import pandas as pd
import json
import requests
from datetime import datetime, timezone
import additional_py_files.common as common
import random
import logging

sys.path.append("/home/pi/.local/lib/python3.11/site-packages")

from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict

# Configure logging
logging.basicConfig(
    level=common.get_log_level(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("subway_connect")


def api_pull(line, link):
    try:
        logger.debug(f"Conducting API pull of {line}")
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(link)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        feed.ParseFromString(response.content)
        feed = MessageToDict(feed)
        logger.debug(f"Cleaning info for {line}")
        clean_info = subway_cleanup(feed)
        logger.debug(f"Completed cleaning up {line}")
        return clean_info
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during API pull of {line}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during API pull of {line}: {e}")


def all_train_data():
    logger.debug("Starting all train data")
    api_links = [
        {
            "line": "ACE",
            "link": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace",
        },
        {
            "line": "BDFM",
            "link": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm",
        },
        {
            "line": "G",
            "link": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g",
        },
        {
            "line": "JZ",
            "link": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz",
        },
        {
            "line": "NQRW",
            "link": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw",
        },
        {
            "line": "L",
            "link": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l",
        },
        {
            "line": "1234567",
            "link": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs",
        },
        {
            "line": "SIR",
            "link": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-si",
        },
    ]
    all_train_info = []
    for x in api_links:
        trains = api_pull(x["line"], x["link"])
        if trains:
            for i in trains:
                all_train_info.append(i)
            logger.debug(f"Added information from the {x['line']} line.")
        else:
            logger.warning(f"No data returned for the {x['line']} line.")
    if all_train_info:
        data_dump(all_train_info)
    else:
        logger.warning("No train data was collected from any line.")
    return all_train_info


def data_dump(train_info):
    data_dict = {}
    try:
        for x in train_info:
            train_id = x["id"]
            data_dict.update({train_id: x})
        with open("data/subway_info.json", "w") as json_file:
            json.dump(data_dict, json_file, indent=4)
        logger.debug("Successfully dumped train data to a json")
    except BaseException:
        logger.error("ERROR converting train data to a json")


def next_train_in_v2(station, data):
    station_object = common.build_station_element(station)
    train_stops = []
    now = datetime.now()
    logger.debug(f"Time now: {now}")
    for x in data:
        try:
            for y in x["tripUpdate"]["stopTimeUpdate"]:
                stop_id = y["stopId"]
                if (
                    stop_id in station_object["stop_ids"]
                    or str(stop_id + "S") in station_object["stop_ids"]
                    or str(stop_id + "N") in station_object["stop_ids"]
                ):
                    route = x["tripUpdate"]["trip"]["routeId"]
                    tripID = x["tripUpdate"]["trip"]["tripId"]
                    final_dest = x["tripUpdate"]["stopTimeUpdate"][-1]["stop_name"]
                    arrival_time = datetime.fromtimestamp(int(y["arrival"]["time"]))
                    difference = arrival_time - now
                    arrival_time = int(difference.total_seconds() / 60)
                    if arrival_time < 0:
                        pass
                    else:
                        route_info = {
                            "route": route,
                            "tripId": tripID,
                            "final_dest": final_dest,
                            "arrival": arrival_time,
                            "station_info": y,
                        }
                        train_stops.append(route_info)
        except BaseException:
            pass
    train_stops.sort(key=lambda k: k["arrival"])
    logger.debug("Next train in complete")
    return train_stops


def random_station_v2():
    all_stations = common.stations_load_v2()
    while True:
        station = random.choice(list(all_stations.keys()))
        if all_stations[station]["enabled"] is True:
            return station


def subway_cleanup(train_info):
    subway_stops = pd.read_csv("data/stations.csv", index_col=None, header=0)
    subway_stops = subway_stops.set_index("stop_id")
    stop_time_update = []
    for x in train_info["entity"]:
        try:
            x["tripUpdate"]["stopTimeUpdate"]
            stop_time_update.append(x)
        except BaseException:
            pass
    for x in stop_time_update:
        for y in x["tripUpdate"]["stopTimeUpdate"]:
            try:
                stop_id = y["stopId"]
                stop_name = subway_stops.loc[stop_id][1]
                y.update({"stop_name": stop_name})
            except BaseException:
                pass
    return stop_time_update
