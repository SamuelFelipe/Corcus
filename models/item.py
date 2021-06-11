#!/usr/bin/python3 

'''Employee Class Definition'''

from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship


class Item(BaseModel, Base):

    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250), nullable=False)
    unitary_value = Column(Float, nullable=False)
    finished = Column(Float, default=0)
    employee_id = Column(ForeignKey('employes.id'))
    employee = relationship('Employee', back_populates='item')
