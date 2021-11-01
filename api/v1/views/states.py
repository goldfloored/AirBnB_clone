#!/usr/bin/python3
"""
    API view related to State objects that handles all the default
    actions.
"""
from api.v1.views import app_views
from models import storage
from models.state import State
import json
from werkzeug.exceptions import BadRequest, NotFound
from flask import request, jsonify, make_response, abort
from flasgger import swag_from


@app_views.route('/states', methods=['GET'])
@swag_from('../swagger_configs/states/list.yml')
def states_list() -> json:
    """
    Retrieves the list of all State objects.

    Returns:
        json: List of State objects with status code 200.
    """
    states = storage.all(State)
    list = []
    for key, state in states.items():
        list.append(state.to_dict())
    return make_response(jsonify(list), 200)


@app_views.route('/states/<state_id>', methods=['GET'])
@swag_from('../swagger_configs/states/show.yml')
def state_show(state_id) -> json:
    """
    Retrieves a specified State object.

    Args:
        state_id : ID of the wanted State object.

    Raises:
        NotFound: Raises a 404 error if state_id
        is not linked to any State object.

    Returns:
        json: Wanted State object with status code 200.
    """
    state = storage.get(State, state_id)

    if state is None:
        raise NotFound

    return make_response(jsonify(state.to_dict()), 200)


@app_views.route('/states/<state_id>', methods=['DELETE'])
@swag_from('../swagger_configs/states/delete.yml')
def state_delete(state_id) -> json:
    """
    Deletes a specified State object.

    Args:
        state_id : ID of the wanted State object.

    Raises:
        NotFound: Raises a 404 error if state_id
        is not linked to any State object.

    Returns:
        json: Empty dictionary with the status code 200.
    """
    state = storage.get(State, state_id)

    if state is None:
        raise NotFound

    state.delete()
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/', methods=['POST'])
@swag_from('../swagger_configs/states/create.yml')
def state_create() -> json:
    """
    Creates a new State object.

    Error cases:
        BadRequest: If the given data is not a
        valid json or if the key 'name' is not
        present sends status code 400.

    Returns:
        json: The new State with the status code 201.
    """
    if not request.json:
        return make_response('Not a JSON', 400)

    if 'name' not in request.get_json().keys():
        return make_response('Missing name', 400)

    state = State(**request.get_json())
    state.save()

    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
@swag_from('../swagger_configs/states/update.yml')
def state_update(state_id) -> json:
    """
    Update a specified State object.

    Args:
        state_id : Id of the wanted State object.

    Returns:
        json: The updated State object with the status code 200.
    """
    state = storage.get(State, state_id)

    if state is None:
        raise NotFound

    if not request.json:
        return make_response('Not a JSON', 400)

    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            state.__setattr__(key, value)

    state.save()

    return make_response(jsonify(state.to_dict()), 200)
