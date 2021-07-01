#!/usr/bin/python3
"""This module contains Review class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """
    Review class inheriting from basemodel
    """
    place_id = ""
    user_id = ""
    text = ""
