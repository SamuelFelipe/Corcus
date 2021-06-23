#!/usr/bin/python3

'''
Base model to define common methods and atributes.

Atributes:
    created_at = the date when the object was created
    updated_at = the last object modification date

Methods:
    save() = save the object into the data base
    delete() = delete the object
    to_dict() = return a dictionaty version of the object
'''

from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy import inspect
import models
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    '''BaseModel declaration'''

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    def save(self):
        '''Save hte object into the data base'''
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def __str__(self):
        '''Returs a string format of the object
Format = [<Class name>]{Atributes dictionary}
'''
        return '[{}]{}'.format(self.__class__.__name__,
                               self.to_dict())

    def delete(self):
        '''Removes the object, to make it Permanent needs to commit'''
        models.storage.delete(self)

    def to_dict(self):
        '''Removes sensible data an return a dictionary'''
        ret = self.__dict__.copy()
        if 'company' in ret:
            del ret['company']
        if '_sa_instance_state' in ret:
            del ret['_sa_instance_state']
        if 'created_at' in ret:
            ret['created_at'] = ret['created_at'].strftime(time)
        if 'updated_at' in ret:
            ret['updated_at'] = ret['updated_at'].strftime(time)
        if 'password_hash' in ret:
            del ret['password_hash']
        return ret
