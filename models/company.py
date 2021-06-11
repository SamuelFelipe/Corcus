#!/usr/bin/python3 

'''Employee Class Definition'''

from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
import uuid


class Company(BaseModel, Base):
    '''
'''

    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, index=True)
    admin_user = relationship('Admin', uselist=False, back_populates='company')
    employees = relationship('Employee')
