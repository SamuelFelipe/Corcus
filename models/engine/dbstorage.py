#!/usr/bin/python3

'''DataBase Administrator with SQLAlchemy

Atributes:
    __engine
    __session

Methods:
    reload() = read the database and create all the storage objects
    all(cls=None) = return all the object for a class, if class is null,
                    return all the storaged objects
    new(obj) = create a new object
    save() = commit all the changes into the database
    delete() = remove the passed object
    close() = closes the actual session
'''

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
    '''Engine to administrate the DataBases'''

    __engine = None
    __session = None

    def __init__(self):
        '''Read the env variables and start to storage'''
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
        '''Reload all the objects'''
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def all(self, cls=None):
        '''Return all the objects from a class if it's not None
otherwise return all the objects
'''
        ret = {}
        for cl in classes.values():
            if cls is None or cls == cl:
                objs = self.__session.query(cl).all()
                for obj in objs:
                    ret[obj.id] = obj
        return ret

    def new(self, obj):
        '''Create a  new object'''
        self.__session.add(obj)

    def save(self):
        '''Save all the resent changes'''
        self.__session.commit()

    def delete(self, obj=None):
        '''Delete the passed object'''
        if obj is not None:
            self.__session.delete(obj)

    def close(self):
        '''Close the session'''
        self.__session()
