#!/usr/bin/python3
"""This module contains Place class."""
from models.base_model import BaseModel


class Place(BaseModel):
    """
    Place class inherits from BaseModel
    Attributes:
        NAME:           TYPE:   DESC:
        city_id         (str)   id of city
        user_id         (str)   id of user
        name            (str)   name of place
        description     (str)   description of place
        number_rooms    (int)   number of rooms of place
        number_bathrooms(int)   number of bathrooms of place
        max_guest       (int)   maximum number of guests
        price_by_night  (int)   price by night of place
        latitude        (float) the latitude of place
        longitude       (float) the longitude of place
        amenity_ids     (list)  list of strings detailing amenities
    """
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
