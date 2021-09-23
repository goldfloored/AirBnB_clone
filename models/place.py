#!/usr/bin/python3
"""This is the place class"""
from models.base_model import Base, BaseModel
import models
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from os import getenv


class Place(BaseModel, Base):
    """This is the class for Place
    Attributes:
        city_id: city id
        user_id: user id
        name: name input
        description: string of description
        number_rooms: number of room in int
        number_bathrooms: number of bathrooms in int
        max_guest: maximum guest in int
        price_by_night:: pice for a staying in int
        latitude: latitude in flaot
        longitude: longitude in float
        amenity_ids: list of Amenity ids
    """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    place_amenity = Table('place_amenity', Base.metadata, Column(
                'place_id', String(60), ForeignKey(
                    'places.id'), primary_key=True, nullable=False), Column(
                    'amenity_id', String(60), ForeignKey(
                        'amenities.id'), primary_key=True, nullable=False))

    reviews = relationship(
            "Review", backref='place', cascade="all, delete, delete-orphan")

    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenities = relationship(
                "Amenity", secondary='place_amenity', viewonly=False)

    else:
        @property
        def amenities(self):
            """ return list of amenities that certain place has"""
            all_objs = models.storage.all()
            amenities_list = []
            for k, v in all_objs.items():
                if v.__class__.__name__ == 'Amenity' and \
                                         v.id in self.amenity_ids:
                    amenities_list.append(v)
            return amenities_list

        @amenities.setter
        def amenties(self):
            """ add Amenity.id to amenity_ids list"""
            if self.__class__.__name__ is not 'Amenity':
                return
            amenity_ids.append(self.id)

        @property
        def reviews(self):
            """ gets a list of review objects from that place """
            all_obj = models.storage.all()
            reviews_list = []
            for k, v in all_obj.items():
                if v.__class__.__name__ == 'Review' and v.place_id == self.id:
                    reviews_list.append(v)
            return reviews_list
