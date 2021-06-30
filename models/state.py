#!/usr/bin/python3
"""This module contains State class."""
from models.base_model import BaseModel


class State(BaseModel):
    """
    State class inherits from BaseModel
    Attributes:
        NAME:   TYPE:   DESC:
        name    (str)   state name
    """
    name = ""
