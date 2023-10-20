#!/usr/bin/python3
"""DataBase Storage Module"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """class defination for dbstorage engine"""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        conn = f"mysql+mysqldb://{user}:{passwd}@{host}/{db}"
        self.__engine = create_engine(conn, pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        queries on the current database session
        all objects depending of the class name
        """
        classes = ("User", "State", "City", "Amenity", "Place", "Review")
        session = self.__session
        dictionary = {}

        if cls is None:
            for item in classes:
                query = session.query(item)
                for obj in query.all():
                    key = f"{obj.__class__.__name}.{obj.id}"
                    dictionary[key] = obj
        else:
            query = session.query(cls)
            for obj in query.all():
                key = f"{obj.__class__.__name}.{obj.id}"
                dictionary[key] = obj

        return dictionary

    def new(self, obj):
        """add the object to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        create all tables in the database
        and the current database session
        """
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)

        self.__session = Session()

    def close(self):
        """closes the working SQLAlchemy session"""
        self.__session.close()
