#!/usr/bin/python3 

'''Bonus Class Definition'''

from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship


class Bonus(BaseModel, Base):
    '''
Bonus class.


        Atributes:
            id - Bonus id
            type - type/name of the bonus
            description - bonus description
            value - value to add to the user payment
'''

    __tablename__ = 'bonus'
    id = Column(Integer, primary_key=True)
    type = Column(String(80), nullable=False)
    description = Column(String(250))
    value = Column(Float, nullable=False)
    employee_id = Column(ForeignKey('employes.id'))
    employee = relationship('Employee', back_populates='bonus')
