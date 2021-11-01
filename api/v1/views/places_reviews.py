#!/usr/bin/python3
"""
    API view related to Review objects that handles all the default
    actions.
"""
import requests
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
import json
from werkzeug.exceptions import BadRequest, NotFound
from flask import Flask, request, jsonify, make_response
from flasgger import swag_from


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
@swag_from('../swagger_configs/places_reviews/list.yml')
def reviews_list(place_id) -> json:
    """
    Retrieves the list of all Review objects.

    Returns:
        json: List of Review objects with status code 200.
    """
    place = storage.get(Place, place_id)

    if place is None:
        raise NotFound

    reviews = place.reviews

    list = []
    for review in reviews:
        list.append(review.to_dict())
    return make_response(jsonify(list), 200)


@app_views.route('/reviews/<review_id>', methods=['GET'])
@swag_from('../swagger_configs/places_reviews/show.yml')
def review_show(review_id) -> json:
    """
    Retrieves a specified Review object.

    Args:
        review_id : ID of the wanted Review object.

    Raises:
        NotFound: Raises a 404 error if review_id
        is not linked to any Review object.

    Returns:
        json: Wanted Review object with status code 200.
    """
    review = storage.get(Review, review_id)

    if review is None:
        raise NotFound

    return make_response(jsonify(review.to_dict()), 200)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
@swag_from('../swagger_configs/places_reviews/delete.yml')
def review_delete(review_id) -> json:
    """
    Deletes a specified Review object.

    Args:
        review_id : ID of the wanted Review object.

    Raises:
        NotFound: Raises a 404 error if review_id
        is not linked to any Review object.

    Returns:
        json: Empty dictionary with the status code 200.
    """
    review = storage.get(Review, review_id)

    if review is None:
        raise NotFound

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews/', methods=['POST'])
@swag_from('../swagger_configs/places_reviews/create.yml')
def review_create(place_id) -> json:
    """
    Creates a new Review object.

    Error cases:
        BadRequest: If the given data is not a
        valid json or if the key 'email' or 'password'
        is not present sends status code 400.

    Returns:
        json: The new Review with the status code 201.
    """
    place = storage.get(Place, place_id)

    if place is None:
        raise NotFound

    if not request.json:
        return make_response('Not a JSON', 400)

    if 'user_id' not in request.get_json().keys():
        return make_response('Missing user_id', 400)

    user = storage.get(User,  request.get_json()['user_id'])

    if user is None:
        raise NotFound

    if 'text' not in request.get_json().keys():
        return make_response('Missing text', 400)

    data = request.get_json()
    data['place_id'] = place_id
    review = Review(**data)

    review.save()

    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
@swag_from('../swagger_configs/places_reviews/update.yml')
def review_update(review_id) -> json:
    """
    Update a specified Review object.

    Args:
        review_id : Id of the wanted State object.

    Returns:
        json: The updated State object with the status code 200.
    """
    review = storage.get(Review, review_id)

    if review is None:
        raise NotFound

    if not request.json:
        return make_response('Not a JSON', 400)

    for key, value in request.get_json().items():
        if key not in ('id', 'place_id', 'created_at', 'updated_at'):
            review.__setattr__(key, value)

    review.save()

    return make_response(jsonify(review.to_dict()), 200)
