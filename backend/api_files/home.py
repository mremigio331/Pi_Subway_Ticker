from flask import jsonify


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
