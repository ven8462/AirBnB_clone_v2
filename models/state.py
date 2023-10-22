#!/usr/bin/python3
""" State Module for HBNB project """
import os
import models
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship(
            'City',
            backref='state',
            cascade="all, delete, delete-orphan")
    else:
        @property
        def cities(self):
            """getter for cities related to state"""
            # from models.__init__ import storage
            # from models.city import City
            cit_list = []
            city_stor = models.storage.all(City).values()
            for val in city_stor:
                if self.id == val.state_id:
                    cit_list.append(val)
            return cit_list
