import additional_py_files.constants as constants
import additional_py_files.common as common
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_caching import Cache
import threading
import sys
sys.path.append('additional_py_files')
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
@cache.cached(timeout=10)
def pi_api_home():
    # curl -H "Content-Type: application/json" http://localhost:5000/
    try:
        welcome_message = (
            'Welcome to the locally hosted endpoint '
            + 'for your Pi Subway Tracker')
        return (
            jsonify(welcome_message),
            200,
            {'Content-Type': 'application/json'}
        )

    except Exception as e:
        error = str(e)
        return jsonify(error), 500, {'Content-Type': 'application/json'}


@app.route('/trains/current_station', methods=[constants.GET])
@cache.cached(timeout=10)
def get_current_station():
    if request.method == constants.GET:
        # curl -i -X GET -H "Content-Type: application/json" http://localhost:5000/trains/current_station
        # curl -i -X PUT -H "Content-Type: application/json" http://localhost:5000/trains/current_station

        try:
            all_trains_data = common.open_json_file(constants.API_EXPORT_FILE)
            current_station = {
                constants.CURRENT_STATION: (
                    all_trains_data[constants.CURRENT_STATION]
                )
            }
            return (
                jsonify(current_station),
                200,
                {'Content-Type': 'application/json'}
            )

        except Exception as e:
            error = str(e)
            return jsonify(error), 500, {'Content-Type': 'application/json'}


@app.route('/trains/current_station', methods=[constants.PUT])
@cache.cached(timeout=10)
def update_current_station():
    # curl -i -X PUT -H "station: Times Sq-42 St - R16" -H "cycle: false" http://localhost:5000/trains/current_station
    # curl -i -X PUT -H "force_change_station: 103 St - 119" -H "cycle: true" http://localhost:5000/trains/current_station
    if request.method == constants.PUT:
        if (
            (constants.STATION not in request.headers)
            and
            (constants.FORCE_CHANGE_STATION not in request.headers)
        ):
            return_message = {
                'error': (
                    'Header is missing one of the following: '
                    + f' {constants.STATION} or '
                    + f'{constants.FORCE_CHANGE_STATION}'
                )
            }
            return (
                jsonify(return_message),
                400,
                {'Content-Type': 'application/json'}
            )

        if (
            (constants.STATION in request.headers)
            and
            (constants.FORCE_CHANGE_STATION in request.headers)
        ):
            return_message = {
                'error': (
                    'Can only pass one of the following headers: '
                    + f' {constants.STATION} or '
                    + f'{constants.FORCE_CHANGE_STATION}'
                )
            }
            return (
                jsonify(return_message),
                400,
                {'Content-Type': 'application/json'}
            )

        elif constants.CYCLE not in request.headers:
            return_message = {
                'error': f'{constants.CYCLE} header is missing'}
            return (
                jsonify(return_message),
                400,
                {'Content-Type': 'application/json'}
            )

        all_trains_data = common.open_json_file(constants.API_EXPORT_FILE)
        all_config = common.open_json_file(constants.CONFIG_FILE)
        current_station = all_trains_data[constants.CURRENT_STATION]
        current_cycle = all_config[constants.CYCLE]
        new_cycle = str_to_bool(request.headers.get(constants.CYCLE))

        if constants.STATION in request.headers:
            new_station = request.headers.get(constants.STATION)
            if common.station_check_v2(new_station) is False:
                return (
                    jsonify(
                        {'error': (
                            f'{new_station} not found. Ensure you '
                            + 'are using the stop name with the stop id')}
                    ),
                    404
                )
            if (
                (current_station == new_station)
                and
                (new_cycle == current_cycle)
            ):
                message = (
                    'Configs are already set to '
                    + f'current_station {current_station}'
                    + f'cycle: {new_cycle}. No changes made'
                )
                return jsonify(message), 204

        elif constants.FORCE_CHANGE_STATION in request.headers:
            new_station = request.headers.get(constants.FORCE_CHANGE_STATION)
            if common.station_check_v2(new_station) is False:
                return (
                    jsonify(
                        {'error': (
                            f'{new_station} not found. Ensure you '
                            + 'are using the stop name with the stop id')}
                    ),
                    404
                )
            if (
                (current_station == new_station)
                and
                (new_cycle == current_cycle)
            ):
                message = (
                    'Configs are already set to '
                    + f'current_station {current_station}'
                    + f'cycle: {new_cycle}. No changes made'
                )
                return jsonify(message), 204

        try:

            if constants.STATION in request.headers:
                all_config[constants.STATION] = new_station
                all_config[constants.CYCLE] = new_cycle
                message = (
                    'Successfully updated the current station to '
                    + f'{new_station} and cycle to {new_cycle}.'
                )

            elif constants.FORCE_CHANGE_STATION in request.headers:
                all_config[constants.FORCE_CHANGE_STATION] = new_station
                all_config[constants.CYCLE] = new_cycle
                message = (
                    f'Successfully updated the force_change to '
                    f'{new_station} and cycle to {new_cycle}.'
                )

            common.update_json(constants.CONFIG_FILE, all_config)
            return (
                jsonify(message),
                200,
                {'Content-Type': 'application/json'}
            )

        except Exception as e:
            error = str(e)
            return jsonify(error), 500, {'Content-Type': 'application/json'}


@app.route('/trains/next_four', methods=[constants.GET])
@cache.cached(timeout=10)
def get_next_four():
    if request.method == constants.GET:
        # curl -i -X GET -H "Content-Type: application/json" http://localhost:5000/trains/next_four
        try:
            all_trains_data = common.open_json_file(constants.API_EXPORT_FILE)
            next_four_info = {
                constants.CURRENT_STATION: common.build_station_element(all_trains_data[constants.CURRENT_STATION]),
                constants.NEXT_FOUR: all_trains_data[constants.NEXT_FOUR],
                constants.TIMESTAMP: all_trains_data[constants.TIMESTAMP],
                constants.LOADING: all_trains_data[constants.LOADING],
            }
            return (
                jsonify(next_four_info),
                200,
                {'Content-Type': 'application/json'}
            )

        except Exception as e:
            error = str(e)
            return jsonify(error), 500, {'Content-Type': 'application/json'}


@app.route('/trains/all_data', methods=[constants.GET])
@cache.cached(timeout=10)
def get_all_trains_data():
    if request.method == constants.GET:
        # curl -i -X GET -H "Content-Type: application/json" http://localhost:5000/trains/all_data
        try:
            all_trains_data = common.open_json_file(constants.API_EXPORT_FILE)
            return (
                jsonify(all_trains_data),
                200,
                {'Content-Type': 'application/json'}
            )

        except Exception as e:
            error = str(e)
            return jsonify(error), 500, {'Content-Type': 'application/json'}


@app.route('/trains/stations/full_info', methods=[constants.GET])
@cache.cached(timeout=10)
def get_all_train_stations():
    if request.method == constants.GET:
        # curl -i -X GET -H "Content-Type: application/json" http://localhost:5000/trains/stations/full_info
        try:
            all_train_stations = common.stations_load_v2()
            return (
                jsonify(all_train_stations),
                200,
                {'Content-Type': 'application/json'}
            )

        except Exception as e:
            error = str(e)
            return (
                jsonify(error),
                500,
                {'Content-Type': 'application/json'}
            )


@app.route('/trains/stations/specific_station', methods=[constants.GET, constants.PUT])
@cache.cached(timeout=10)
def specific_station_info():
    if constants.STATION not in request.headers:
        return jsonify({'error': 'Station header is missing'}), 400

    if request.method == constants.GET:
        # curl -i -X GET -H "station: 161 St-Yankee Stadium - D11" http://localhost:5000/trains/stations/specific_station
        try:
            specific_train_station = request.headers.get(constants.STATION)
            if common.station_check_v2(specific_train_station) is False:
                return (
                    jsonify(
                        {'error': (
                            f'{specific_train_station} not found. Ensure you '
                            + 'are using the stop name with the stop id')}
                    ),
                    404
                )

            all_train_stations = common.stations_load_v2()
            return (
                jsonify(all_train_stations[specific_train_station]),
                200,
                {'Content-Type': 'application/json'}
            )

        except Exception as e:
            error = str(e)
            return (
                jsonify(error),
                500,
                {'Content-Type': 'application/json'}
            )

    if request.method == constants.PUT:
        # curl -i -X PUT -H "station: 161 St-Yankee Stadium - D11" -H "enabled: false" http://localhost:5000/trains/stations/specific_station
        if constants.ENABLED not in request.headers:
            return jsonify({'error': 'Enabled header is missing'}), 400

        updated_enabled = str_to_bool(
            request.headers.get(constants.ENABLED)
        )
        try:
            specific_train_station = request.headers.get(constants.STATION)
            if common.station_check_v2(specific_train_station) is False:
                return (
                    jsonify(
                        {'error': (
                            f'{specific_train_station} not found. Ensure you '
                            + 'are using the stop name with the stop id')}
                    ),
                    404
                )

            all_train_stations = common.stations_load_v2()
            highlighted_station = all_train_stations[specific_train_station]
            highlighted_station[constants.ENABLED] = updated_enabled
            all_train_stations[specific_train_station] = highlighted_station
            common.update_json(constants.STATIONS_FILE, all_train_stations)

            return_message = {
                'message': (
                    f'Successfully updated {specific_train_station} station '
                    + f'status to {updated_enabled}'
                ),
                'updated_data': highlighted_station
            }
            return jsonify(return_message), 200, {'Content-Type': 'application/json'}

        except Exception as e:
            error = str(e)
            return (
                jsonify(error),
                500,
                {'Content-Type': 'application/json'}
            )


@app.route('/config', methods=[constants.GET])
@cache.cached(timeout=10)
def get_all_config():
    if request.method == constants.GET:
        # curl -i -X GET -H "Content-Type: application/json" http://localhost:5000/config
        # curl -i -X PUT -H "Content-Type: application/json" http://localhost:5000/config
        try:
            all_config = common.open_json_file(constants.CONFIG_FILE)
            config_list = common.dict_to_list_of_dicts(all_config)
            return jsonify(config_list), 200, {'Content-Type': 'application/json'}
        except Exception as e:
            error = str(e)
            return jsonify(error), 500, {'Content-Type': 'application/json'}


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method Not Allowed'}), 405


def str_to_bool(string):
    # Convert the string to lowercase for case-insensitive comparison
    string_lower = string.lower()

    # Check if the string is "true" or "false" and return the corresponding boolean value
    if string_lower == 'true':
        return True
    elif string_lower == 'false':
        return False
    else:
        raise ValueError("Input string must be 'true' or 'false'")


def run_flask():
    app.run(threaded=True)


if __name__ == '__main__':
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
