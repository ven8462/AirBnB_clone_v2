#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", backref="state", cascade="all, delete")
    else:
        @property
        def cities(self):
            """
            getter attribute cities that returns
            the list of City instances with state_id
            equals to the current State.id
            """
            from models import storage
            obj = storage.all(City)
            city_list = []
            for value in obj.values():
                if value.state_id == self.id:
                    city_list.append(value)

            return city_list
