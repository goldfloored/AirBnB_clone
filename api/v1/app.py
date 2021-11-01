#!/usr/bin/python3
"""
    Main API application
"""
from os import getenv
from werkzeug.exceptions import NotFound
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import storage
from flasgger import Swagger


app = Flask(__name__)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
swagger = Swagger(app)


@app.teardown_appcontext
def teardown(exception):
    """
        Call close function from storage in order to
        close current SQLAlchemy session.
    """
    storage.close()


@app.errorhandler(NotFound)
def handle_not_found(e):
    """
    Handle 404 Not found error

    Args:
        e: exception

    Returns:
        404 status code
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    # runs the Flask application through port 5000 from local host
    app.run(getenv('HBNB_API_HOST', '0.0.0.0'),
            getenv('HBNB_API_PORT', '5000'), threaded=True)
