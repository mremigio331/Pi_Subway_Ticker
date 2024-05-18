import additional_py_files.constants as constants

import api_files.home as home
import api_files.trains as trains
import api_files.stations as stations
import api_files.configs as configs
import api_files.system as system_actions
from flask import Flask, jsonify
from flask_cors import CORS
import threading
import sys
import os

cwd = sys.argv[0]
if '/' in cwd:
    mvwd = cwd.split(str('/' + os.path.basename(__file__)))[0]
    os.chdir(mvwd)
sys.path.append('additional_py_files')
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def pi_api_home():
    return home.pi_api_home()


@app.route('/trains/current_station', methods=[constants.GET])
def get_current_station():
    return trains.get_current_station()


@app.route('/trains/current_station/update', methods=[constants.PUT])
def update_current_station():
    # curl -i -X PUT -H "station: Times Sq-42 St - R16" -H "cycle: false" http://localhost:5000/trains/current_station/update
    # curl -i -X PUT -H "force_change_station: 103 St - 119" -H "cycle: true"
    # http://localhost:5000/trains/current_station/update
    return trains.update_current_station()


@app.route('/trains/next_four', methods=[constants.GET])
def get_next_four():
    # curl -i -X GET -H "Content-Type: application/json"
    # http://localhost:5000/trains/next_four
    return trains.get_next_four()


@app.route('/trains/all_data', methods=[constants.GET])
def get_all_trains_data():
    # curl -i -X GET -H "Content-Type: application/json"
    # http://localhost:5000/trains/all_data
    return trains.get_all_trains_data()


@app.route('/stations/full_info', methods=[constants.GET])
def get_all_train_stations():
    # curl -i -X GET -H "Content-Type: application/json"
    # http://localhost:5000/stations/full_info
    return stations.get_all_train_stations()


@app.route('/stations/specific_station',
           methods=[constants.GET, constants.PUT])
def specific_station_info():
    # curl -i -X GET -H "station: 161 St-Yankee Stadium - D11" http://localhost:5000/stations/specific_station
    # curl -i -X PUT -H "station: 161 St-Yankee Stadium - D11" -H "enabled:
    # false" http://localhost:5000/stations/specific_station
    return stations.specific_station_info()


@app.route('/configs', methods=[constants.GET])
def get_all_configs():
    # curl -i -X GET -H "Content-Type: application/json" http://localhost:5000/configs
    # curl -i -X PUT -H "Content-Type: application/json"
    # http://localhost:5000/configs
    return configs.get_all_configs()


@app.route('/configs/<config>', methods=[constants.GET, constants.PUT])
def specific_config(config):
    # curl -i -X GET http://localhost:5000/configs/api_key
    # curl -i -X PUT -H "value: true" http://localhost:5000/configs/cycle
    return configs.specific_config(config)


@app.route('/system/restart', methods=[constants.PUT])
def system_restart():
    return system_actions.system_restart()


@app.route('/system/update/pi', methods=['GET'])
def system_update():
    return system_actions.system_update()


@app.route('/system/update/code', methods=[constants.PUT])
def pi_update():
    return system_actions.pi_update()


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method Not Allowed'}), 405


def run_flask():
    app.run(threaded=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
