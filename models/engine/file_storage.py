#!/usr/bin/python3

"""
Contains the FileStorage class
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    a class to serialize and deserialize
    - instance to JSON file
    - to JSON file to instance
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        returns the dictionary
        """
        return self.__objects

    def new(self, obj):
        """
        sets in __objects the obj with key <obj class name>.id
        """
        k = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[k] = obj

    def save(self):
        """
        serializes __objects to the JSON file
        """
        dict_dict = {}
        with open(self.__file_path, 'w') as f:
            for obj in self.all().values():
                k = "{}.{}".format(obj.__class__.__name__, obj.id)
                dict_dict[k] = obj.to_dict()
            json.dump(dict_dict, f)

    def reload(self):
        """
        deserializes the JSON file to __objects
        """
        try:
            with open(self.__file_path) as f:
                dict_dict = json.load(f)
                for key, value in dict_dict.items():
                    k = key.split('.')
                    class_name = k[0]
                    self.new(eval("{}".format(class_name))(**value))
        except FileNotFoundError:
            pass
