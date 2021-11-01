#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __encode_md5(self, string: str) -> str:
        """
            Encode a string with md5
        """
        md5 = hashlib.md5()
        md5.update(string.encode('utf-8'))

        return md5.hexdigest()

    def __setattr__(self, name, value):
        """
            Encode password at init and update
        """
        if name == 'password':
            if (
                not hasattr(self, 'password') or
                value != getattr(self, 'password')
            ):
                value = self.__encode_md5(value)

        super(User, self).__setattr__(name, value)
