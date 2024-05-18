from flask import jsonify


def system_restart():
    return_dict = {'message': 'Not quite ready to restart yet'}
    return jsonify(return_dict), 200, {'Content-Type': 'application/json'}

    # return jsonify(return_dict), 200, {'Content-Type': 'application/json'}
    # try:
    #     subprocess.run(['sudo', 'reboot'])
    #     return jsonify({'message': 'Raspberry Pi is restarting...'}), 200
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500


def system_update():
    return_dict = {'message': 'Not quite ready to update the system yet'}
    return jsonify(return_dict), 200, {'Content-Type': 'application/json'}

    # def generate():
    #    command = ["sudo", "apt", "update"]
    #
    #    # Open a subprocess for the command
    #    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    #
    #    # Stream the output of the command line by line
    #    for line in process.stdout:
    #        yield line.strip() + '\n'  # Yield each line of output with a newline character
    #
    # Return a response object that streams the output
    # return Response(stream_with_context(generate()),
    # content_type='text/event-stream')


def pi_update():
    return_dict = {'message': 'Not quite ready to update the pi yet'}
    return jsonify(return_dict), 200, {'Content-Type': 'application/json'}
