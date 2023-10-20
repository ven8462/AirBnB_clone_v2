#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City


class State(BaseModel, Base):
    """ State class """
    # name = ""
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="states", cascade="all, delete")

    @property
    def cities(self):
        """
        returns the list of City instances
        with state_id equals to the current State.id
        """
        from models import storage
        obj = storage.all(City)
        city_list = []
        for value in obj.values():
            if isinstance(value, City) and value.state_id == self.id:
                city_list.append(value)

        return city_list
