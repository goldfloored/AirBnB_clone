#!/usr/bin/python3
"""This module contains Review class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """
    Review class inherits from BaseModel
    Attributes:
        NAME:       TYPE:   DESC:
        place_id    (str)   id of place
        user_id     (str)   id of user
        text        (str)   content of review
    """
    place_id = ""
    user_id = ""
    text = ""
