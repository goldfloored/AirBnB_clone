#!/usr/bin/python3
"""
    API view related to City objects that handles all the default
    actions.
"""
from os import stat
import requests
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
import json
from werkzeug.exceptions import BadRequest, NotFound
from flask import Flask, request, jsonify, make_response, abort


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def places_amenities_list(place_id) -> json:
    """
    Retrieves the list of all Amenities objects linked to Places.

    Args:
        place_id : ID of the wanted Place object.

    Raises:
        NotFound: Raises a 404 error if place_id
        is not linked to any Place object.

    Returns:
        json: List of City objects with status code 200.
    """
    place = storage.get(Place, place_id)

    if place is None:
        raise NotFound

    amenities = place.amenities

    list = []
    for amenity in amenities:
        list.append(amenity.to_dict())
    return make_response(jsonify(list), 200)
