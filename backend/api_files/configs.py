import additional_py_files.constants as constants
import additional_py_files.common as common

from flask import jsonify, request


def get_all_configs():
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


def specific_config(config):
    if request.method == constants.GET:
        # curl -i -X GET http://localhost:5000/configs/api_key
        try:
            all_config = common.open_json_file(constants.CONFIG_FILE)
            return_dict = {
                'requested_config': config,
                'value': all_config[config]
            }
            return jsonify(return_dict), 200, {'Content-Type': 'application/json'}
        except Exception as e:
            error = str(e)
            return jsonify(error), 500, {'Content-Type': 'application/json'}
    if request.method == constants.PUT:
        try:

            if constants.VALUE not in request.headers:
                return jsonify({'error': 'Value header is missing'}), 400

            all_configs = common.open_json_file(constants.CONFIG_FILE)
            current_value = all_configs[config]
            new_value = ''
            if config in constants.CONFIG_BOOL_OPTIONS:
                # curl -i -X PUT -H "value: true" http://localhost:5000/configs/cycle
                new_value = common.str_to_bool(
                    request.headers.get(constants.VALUE))
            else:
                new_value = request.headers.get(constants.VALUE)

            if current_value == new_value:
                message = f'Config {config} is already set to {new_value}'
            else:
                message = f'Config {config} has been updated from {current_value} to {new_value} '

            all_configs[config] = new_value
            common.update_json(constants.CONFIG_FILE, all_configs)

            return jsonify(message), 200, {'Content-Type': 'application/json'}

        except Exception as e:
            error = str(e)
            return jsonify(error), 500, {'Content-Type': 'application/json'}
