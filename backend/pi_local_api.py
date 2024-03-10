import additional_py_files.constants as constants
import additional_py_files.common as common
import additional_py_files.subway_connect as sc
from flask import Flask, jsonify, request, make_response
import threading
import sys
sys.path.append('additional_py_files')
app = Flask(__name__)


@app.route('/')
def pi_api_home():
    # curl -H "Content-Type: application/json" http://localhost:5000/
    try:
        welcome_message = (
            'Welcome to the locally hosted endpoint'
            + 'for your Pi Subway Tracker')
        return (
            jsonify(welcome_message),
            200,
            {'Content-Type': 'application/json'}
        )

    except Exception as e:
        error = str(e)
        return jsonify(error), 500, {'Content-Type': 'application/json'}


@app.route('/trains/current_station', methods=[constants.GET_REQUEST])
def get_current_station():
    if request.method == constants.GET_REQUEST:
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


@app.route('/trains/next_four', methods=[constants.GET_REQUEST])
def get_next_four():
    if request.method == constants.GET_REQUEST:
        # curl -i -X GET -H "Content-Type: application/json" http://localhost:5000/trains/next_four
        try:
            all_trains_data = common.open_json_file(constants.API_EXPORT_FILE)
            next_four_info = {
                constants.CURRENT_STATION: all_trains_data[constants.CURRENT_STATION],
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


@app.route('/trains/all_data', methods=[constants.GET_REQUEST])
def get_all_trains_data():
    if request.method == constants.GET_REQUEST:
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

@app.route('/trains/stations/full_info', methods=[constants.GET_REQUEST])
def get_all_train_stations():
    if request.method == constants.GET_REQUEST:
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

@app.route('/trains/stations/specific_station', methods=[constants.GET_REQUEST, constants.PUT_REQUEST])
def specific_station_info():
    if constants.STATION_STR not in request.headers:
        return jsonify({'error': 'Station header is missing'}), 400

    if request.method == constants.GET_REQUEST:
        # curl -i -X GET -H "station: 161 St-Yankee Stadium - D11" http://localhost:5000/trains/stations/specific_station
        try:
            specific_train_station = request.headers.get(constants.STATION_STR)
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

    if request.method == constants.PUT_REQUEST:
        # curl -i -X PUT -H "station: 161 St-Yankee Stadium - D11" -H "enabled: false" http://localhost:5000/trains/stations/specific_station
        if constants.ENABLED_STR not in request.headers:
            return jsonify({'error': 'Enabled header is missing'}), 400

        updated_enabled = str_to_bool(
            request.headers.get(constants.ENABLED_STR)
            )
        try:
            specific_train_station = request.headers.get(constants.STATION_STR)
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
            highlighted_station[constants.ENABLED_STR] = updated_enabled
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


@app.route('/settings', methods=[constants.GET_REQUEST])
def get_all_settings():
    if request.method == constants.GET_REQUEST:
        # curl -i -X GET -H "Content-Type: application/json" http://localhost:5000/settings
        # curl -i -X PUT -H "Content-Type: application/json" http://localhost:5000/settings
        try:
            all_settings = common.open_json_file(constants.SETTINGS_FILE)
            return jsonify(all_settings), 200, {'Content-Type': 'application/json'}
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
