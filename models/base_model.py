#!/usr/bin/python3
"""this package contains the basemodel class"""
import uuid
import datetime
import models


class BaseModel:
    """
    a class basemodel covers all common attributes for
    creating instances and parent of classes
    """

    def __init__(self, *args, **kwargs):
        """
        initializing instance
        """
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
        """
        a string format printing output
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """
        saving instance
        """
        self.updated_at = datetime.datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        to dictionnary
        """
        dic = {}
        for key, value in self.__dict__.items():
            dic[key] = value
        dic['created_at'] = self.created_at.isoformat(sep='T')
        dic['updated_at'] = self.updated_at.isoformat(sep='T')
        dic['__class__'] = self.__class__.__name__
        return dic
