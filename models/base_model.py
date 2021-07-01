#!/usr/bin/python3
"""This module contains the BaseModel class."""
import datetime
import models
import uuid


class BaseModel:
    """
    class BaseModel which defines all common attributes/methods for
    other classes
    """

    def __init__(self, *args, **kwargs):
        """instantiates an instance of class BaseModel"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        if len(kwargs) > 0:
            for key, value in kwargs.items():
                if key == 'created_at':
                    self.created_at = datetime.datetime.strptime(
                        value,
                        '%Y-%m-%dT%H:%M:%S.%f'
                    )
                elif key == 'updated_at':
                    self.updated_at = datetime.datetime.strptime(
                        value,
                        '%Y-%m-%dT%H:%M:%S.%f'
                    )
                elif "__class__" == key:
                    pass
                else:
                    setattr(self, key, value)
        else:
            models.storage.new(self)

    def __str__(self):
        """returns a string with a description of the object"""
        return "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id, self.__dict__
        )

    def save(self):
        """
        updates the public instance attribute updated_at with current datetime
        """
        self.updated_at = datetime.datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        returns a dictionary containing all keys/values of __dict__ of the
        instance
        """
        dictionary = {}
        for key, value in self.__dict__.items():
            dictionary[key] = value
        dictionary['created_at'] = self.created_at.isoformat(sep='T')
        dictionary['updated_at'] = self.updated_at.isoformat(sep='T')
        dictionary['__class__'] = self.__class__.__name__
        return dictionary
