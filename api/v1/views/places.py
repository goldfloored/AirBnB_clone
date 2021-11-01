#!/usr/bin/python3
"""
    API view related to Place objects that handles all the default
    actions.
"""
import requests
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
import json
from werkzeug.exceptions import BadRequest, NotFound
from flask import Flask, request, jsonify, make_response
from flasgger import swag_from


@app_views.route('/cities/<city_id>/places', methods=['GET'])
@swag_from('../swagger_configs/places/list.yml')
def places_list(city_id) -> json:
    """
    Retrieves the list of all Place objects.

    Returns:
        json: List of Place objects with status code 200.
    """
    city = storage.get(City, city_id)

    if city is None:
        raise NotFound

    places = city.places

    list = []
    for place in places:
        list.append(place.to_dict())
    return make_response(jsonify(list), 200)


@app_views.route('/places/<place_id>', methods=['GET'])
@swag_from('../swagger_configs/places/show.yml')
def place_show(place_id) -> json:
    """
    Retrieves a specified Place object.

    Args:
        place_id : ID of the wanted Place object.

    Raises:
        NotFound: Raises a 404 error if place_id
        is not linked to any Place object.

    Returns:
        json: Wanted Place object with status code 200.
    """
    place = storage.get(Place, place_id)

    if place is None:
        raise NotFound

    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places/<place_id>', methods=['DELETE'])
@swag_from('../swagger_configs/places/delete.yml')
def place_delete(place_id) -> json:
    """
    Deletes a specified Place object.

    Args:
        place_id : ID of the wanted Place object.

    Raises:
        NotFound: Raises a 404 error if place_id
        is not linked to any Place object.

    Returns:
        json: Empty dictionary with the status code 200.
    """
    place = storage.get(Place, place_id)

    if place is None:
        raise NotFound

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places/', methods=['POST'])
@swag_from('../swagger_configs/places/create.yml')
def place_create(city_id) -> json:
    """
    Creates a new Place object.

    Error cases:
        BadRequest: If the given data is not a
        valid json or if the key 'email' or 'password'
        is not present sends status code 400.

    Returns:
        json: The new Place with the status code 201.
    """
    city = storage.get(City, city_id)

    if city is None:
        raise NotFound

    if not request.json:
        return make_response('Not a JSON', 400)

    if 'name' not in request.get_json().keys():
        return make_response('Missing name', 400)

    if 'user_id' not in request.get_json().keys():
        return make_response('Missing user_id', 400)

    user = storage.get(User,  request.get_json()['user_id'])

    if user is None:
        raise NotFound

    data = request.get_json()
    data['city_id'] = city_id
    place = Place(**data)

    place.save()

    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
@swag_from('../swagger_configs/places/update.yml')
def place_update(place_id) -> json:
    """
    Update a specified Place object.

    Args:
        state_id : Id of the wanted State object.

    Returns:
        json: The updated State object with the status code 200.
    """
    place = storage.get(Place, place_id)

    if place is None:
        raise NotFound

    if not request.json:
        return make_response('Not a JSON', 400)

    for key, value in request.get_json().items():
        if key not in ('id', 'city_id', 'created_at', 'updated_at'):
            place.__setattr__(key, value)

    place.save()

    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'])
def places_search() -> json:
    kwargs = request.get_json()
    if type(kwargs) is not dict:
        return make_response('Not a JSON', 400)

    places = storage.all(Place)
    places_list = []
    for key, place in places.items():
        places_list.append(place.to_dict())

    if len(request.get_json()) == 0:
        return make_response(jsonify(places_list), 200)

    if (
        'states' in request.get_json().keys() and
        'cities' in request.get_json().keys()
    ):
        for place in places:
            city = storage.get(City, place['city_id'])
            if (
                (
                    city.state_id in request.get_json()['states'] and
                    place['city_id'] in request.get_json()['cities']
                ) or
                place['city_id'] in request.get_json()['cities']
            ):
                del place

        return make_response(jsonify(places_list), 200)

    if 'states' in request.get_json().keys():
        for place in places:
            city = storage.get(City, place['city_id'])
            if city.state_id in request.get_json()['states']:
                del place

        return make_response(jsonify(places_list), 200)

    if 'cities' in request.get_json().keys():
        for place in places:
            if place['city_id'] in request.get_json()['cities']:
                del place

        return make_response(jsonify(places_list), 200)

    return make_response(jsonify({}), 200)
