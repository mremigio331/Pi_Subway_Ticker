import additional_py_files.constants as constants
import additional_py_files.common as common

from flask import jsonify, request


def get_all_train_stations():
    if request.method == constants.GET:
        # curl -i -X GET -H "Content-Type: application/json"
        # http://localhost:5000/stations/full_info
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


def specific_station_info():
    if constants.STATION not in request.headers:
        return jsonify({'error': 'Station header is missing'}), 400

    if request.method == constants.GET:
        # curl -i -X GET -H "station: 161 St-Yankee Stadium - D11"
        # http://localhost:5000/stations/specific_station
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
        # curl -i -X PUT -H "station: 161 St-Yankee Stadium - D11" -H "enabled:
        # false" http://localhost:5000/stations/specific_station
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
            return jsonify(return_message), 200, {
                'Content-Type': 'application/json'}

        except Exception as e:
            error = str(e)
            return (
                jsonify(error),
                500,
                {'Content-Type': 'application/json'}
            )
