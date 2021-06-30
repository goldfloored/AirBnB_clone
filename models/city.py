#!/usr/bin/python3
"""This module contains the City class."""
from models.base_model import BaseModel


class City(BaseModel):
    """
    City class inherits from BaseModel
    Attributes:
        NAME:       TYPE:   DESC:
        state_id    (str)   id of state
        name        (str)   name of city
    """
    state_id = ""
    name = ""
