#!/usr/bin/python3

'''Engine to administrate the DataBases'''

import models
from models.basemodel import BaseModel, Base
from models.bonus import Bonus
from models.employee import Employee
from models.company import Company
from models.admin import Admin
from models.item import Item
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


classes = {'bonus': Bonus, 'employee': Employee, 'item': Item,
           'company': Company, 'admin': Admin}


class DBStorage:
    ''''''

    __engine = None
    __session = None

    def __init__(self):
        CORVUS_MYSQL_USER = getenv('CORVUS_MYSQL_USER')
        CORVUS_MYSQL_PWD = getenv('CORVUS_MYSQL_PWD')
        CORVUS_MYSQL_HOST = getenv('CORVUS_MYSQL_HOST')
        CORVUS_MYSQL_DB = getenv('CORVUS_MYSQL_DB')
        CORVUS_ENV = getenv('CORVUS_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(CORVUS_MYSQL_USER,
                                             CORVUS_MYSQL_PWD,
                                             CORVUS_MYSQL_HOST,
                                             CORVUS_MYSQL_DB))
        if CORVUS_ENV == 'test':
            Base.metadata.drop_all(self.__engine)
           

    def reload(self):
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session


    def all(self, cls=None):
        ret = {}
        for cl in classes.values():
            if cls is None or cls == cl:
                objs = self.__session.query(cl).all()
                for obj in objs:
                    ret[obj.id] = obj
        return ret


    def new(self, obj):
        self.__session.add(obj)


    def save(self):
        self.__session.commit()


    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)


    def close(self):
        self.__session()


    def get(self, cls, id):
        if cls not in classes:
            return None
        clss = models.storage.query(cls)
        for obj in clss:
            if obj.id == id:
                return obj
        return None


    def count(self, cls=None):
        clss = classes.values()

        if not cls:
            count = 0
            for clas in clss:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count
