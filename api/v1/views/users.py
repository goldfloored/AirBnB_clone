#!/usr/bin/python3
"""
    API view related to User objects that handles all the default
    actions.
"""
import requests
from api.v1.views import app_views
from models import storage
from models.user import User
import json
from werkzeug.exceptions import BadRequest, NotFound
from flask import Flask, request, jsonify, make_response
from flasgger import swag_from


@app_views.route('/users', methods=['GET'])
@swag_from('../swagger_configs/users/list.yml')
def users_list() -> json:
    """
    Retrieves the list of all User objects.

    Returns:
        json: List of User objects with status code 200.
    """
    users = storage.all(User)
    list = []
    for key, user in users.items():
        list.append(user.to_dict())
    return make_response(jsonify(list), 200)


@app_views.route('/users/<user_id>', methods=['GET'])
@swag_from('../swagger_configs/users/show.yml')
def user_show(user_id) -> json:
    """
    Retrieves a specified User object.

    Args:
        user_id : ID of the wanted User object.

    Raises:
        NotFound: Raises a 404 error if user_id
        is not linked to any User object.

    Returns:
        json: Wanted User object with status code 200.
    """
    user = storage.get(User, user_id)

    if user is None:
        raise NotFound

    return make_response(jsonify(user.to_dict()), 200)


@app_views.route('/users/<user_id>', methods=['DELETE'])
@swag_from('../swagger_configs/users/delete.yml')
def user_delete(user_id) -> json:
    """
    Deletes a specified User object.

    Args:
        user_id : ID of the wanted User object.

    Raises:
        NotFound: Raises a 404 error if user_id
        is not linked to any User object.

    Returns:
        json: Empty dictionary with the status code 200.
    """
    user = storage.get(User, user_id)

    if user is None:
        raise NotFound

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users/', methods=['POST'])
@swag_from('../swagger_configs/users/create.yml')
def user_create() -> json:
    """
    Creates a new User object.

    Error cases:
        BadRequest: If the given data is not a
        valid json or if the key 'email' or 'password'
        is not present sends status code 400.

    Returns:
        json: The new User with the status code 201.
    """
    if not request.json:
        return make_response('Not a JSON', 400)

    if 'email' not in request.get_json().keys():
        return make_response('Missing email', 400)

    if 'password' not in request.get_json().keys():
        return make_response('Missing password', 400)

    user = User(**request.get_json())
    user.save()

    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
@swag_from('../swagger_configs/users/update.yml')
def user_update(user_id) -> json:
    """
    Update a specified State object.

    Args:
        state_id : Id of the wanted State object.

    Returns:
        json: The updated State object with the status code 200.
    """

    user = storage.get(User, user_id)

    if user is None:
        raise NotFound

    if not request.json:
        return make_response('Not a JSON', 400)

    for key, value in request.get_json().items():
        if key not in ('id', 'created_at', 'updated_at'):
            user.__setattr__(key, value)

    user.save()

    return make_response(jsonify(user.to_dict()), 200)
