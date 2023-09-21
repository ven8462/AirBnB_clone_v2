#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from os import getenv
from sqlalchemy.orm import relationship
from models import Review


class Place(BaseModel, Base):
    """ A place to stay """
    # city_id = ""
    # user_id = ""
    # name = ""
    # description = ""
    # number_rooms = 0
    # number_bathrooms = 0
    # max_guest = 0
    # price_by_night = 0
    # latitude = 0.0
    # longitude = 0.0
    # amenity_ids = []

    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("user.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review",
                               backref="place", cascade="all, delete")
    else:
        @property
        def reviews(self):
            """
            getter attribute reviews that
            returns the list of Review instances
            with place_id equals to the current Place.id
            """
            from models import storage
            obj = storage.all(Review)
            review_list = []
            for value in obj.values():
                if value.place_id == self.id:
                    review_list.append(value)

            return review_list
