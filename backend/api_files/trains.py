import additional_py_files.constants as constants
import additional_py_files.common as common

from flask import jsonify, request


def get_current_station():
    if request.method == constants.GET:
        # curl -i -X GET -H "Content-Type: application/json" http://localhost:5000/trains/current_station
        # curl -i -X PUT -H "Content-Type: application/json"
        # http://localhost:5000/trains/current_station
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


def update_current_station():
    # curl -i -X PUT -H "station: Times Sq-42 St - R16" -H "cycle: false" http://localhost:5000/trains/current_station
    # curl -i -X PUT -H "force_change_station: 103 St - 119" -H "cycle: true"
    # http://localhost:5000/trains/current_station
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
        new_cycle = common.str_to_bool(request.headers.get(constants.CYCLE))

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


def get_next_four():
    if request.method == constants.GET:
        # curl -i -X GET -H "Content-Type: application/json"
        # http://localhost:5000/trains/next_four
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


def get_all_trains_data():
    if request.method == constants.GET:
        # curl -i -X GET -H "Content-Type: application/json"
        # http://localhost:5000/trains/all_data
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
