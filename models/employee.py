#!/usr/bin/python3 

'''Employee Class Definition'''

from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship


class Employee(BaseModel, Base):
    '''
Employee class.


        Atributes:
            id - emloyee identification
            names - emloyee names
            forename - emloyee forenames
            job - emloyee job
            worked_hours - hours in all the month
            bonus - payment considerations
'''

    __tablename__ = 'employes'
    id = Column(String(32), primary_key=True)
    company = Column(ForeignKey('company.id'), nullable=False)
    names = Column(String(80), nullable=False)
    forenames = Column(String(80), nullable=False)
    position = Column(String(80), nullable=False)
    c_type = Column(String(80), nullable=False)
    item = relationship('Item', back_populates='employee')
    risk = Column(String(1), default=1)
    base_salary = Column(Float, default=0)
    worked_hours = Column(Integer, default=0)
    bonus = relationship('Bonus', back_populates='employee')

    def arl(self):
        risks = {'1': 0.522, '2': 1.044, '3': 2.436, '4': 4.35, '5': 6.96}
        return risks[self.risk] * self.base_salary

    def health(self):
        if self.c_type == 'Termino Indefinido':
            return self.base_salary * 0.125
        return 0

    def pension(self):
        if self.c_type == 'Termino Indefinido':
            return self.base_salary * 0.16
        return 0

    def para_f(self):
        if self.c_type == 'Termino Indefinido':
            return self.base_salary * 0.02
        return 0

    def salary(self):
        if self.c_type == 'Obra Labor':
            pass
        return self.salary
