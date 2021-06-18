#!/usr/bin/python3

'''BaseModel class definition'''

from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy import inspect
import models
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    ''''''

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())


    def save(self):
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def __str__(self): 
        return '[{}]{}'.format(self.__class__.__name__,
                               self.to_dict())

    def delete(self):
        models.storage.delete(self)

    def to_dict(self):
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
