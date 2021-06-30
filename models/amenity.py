#!/usr/bin/python3
"""This module is for hbnb Amenity class."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Amenity class inherits from BaseModel
    Attributes:
        NAME:   TYPE:   DESC:
        name    (str)   name of amenity
    """
    name = ""
