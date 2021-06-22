#!/usr/bin/python3 

'''
Employee class.


Atributes:
    id - emloyee identification
    names - emloyee names
    forename - emloyee forenames
    position - emloyee job
    worked_weeks - number of worked weeks
    bonus - payment considerations
    c_type - contract type, it could be [
                                         'Termino Indefinido'
                                         'Obra Labor'
                                         'Prestacion de Servicios'
                                         ]
    risk - level of risk to caculate arl payment
    item - in case of c_type == 'Obra Labor' the payment will be the
           sum of all the employee items
    base_salary - the acorded salaru in the employee contract
    eps - the eps name
    no_acount - number of the account to depositate the month payment
'''

from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship


class Employee(BaseModel, Base):
    '''Employee Class Definition'''

    __tablename__ = 'employes'
    id = Column(String(32), primary_key=True)
    company = Column(ForeignKey('company.id'), nullable=False)
    names = Column(String(80), nullable=False)
    forenames = Column(String(80), nullable=False)
    position = Column(String(80), nullable=False)
    c_type = Column(String(80), nullable=False)
    item = relationship('Item', back_populates='employee')
    risk = Column(String(1), default='1')
    arl_payment = Column(Boolean, default=False)
    base_salary = Column(Float, default=908526)
    worked_weeks = Column(Integer, default=0)
    month_payment = Column(Boolean, default=False)
    eps = Column(String(60), nullable=False)
    bonus = relationship('Bonus', back_populates='employee')
    no_acount = Column(String(120), nullable=False)

    def arl(self):
        '''Calculate the arl payment'''
        if self.c_type in ['Termino Indefinido', 'Prestacion de Servicios']:
            risks = {'1': 0.00522, '2': 0.01044, '3': 0.02436, '4': 0.0435, '5': 0.0696}
            return risks[self.risk] * self.salary()
        return 0

    def health(self):
        '''Calculate the health payment'''
        if self.c_type in ['Termino Indefinido', 'Prestacion de Servicios']:
            return self.salary() * 0.125
        return 0

    def pension(self):
        '''Calculate the pension payment'''
        if self.c_type in ['Termino Indefinido', 'Prestacion de Servicios']:
            return self.salary() * 0.16
        return 0

    def para_f(self):
        '''Calculate 'parafiscales' taxes'''
        if self.c_type in ['Termino Indefinido', 'Prestacion de Servicios']:
            return self.salary() * 0.09
        return 0

    def salary(self):
        '''Depending of the c_type return the salary of the employee'''
        salary = 0
        if self.c_type == 'Obra Labor':
            self.base_salary = 0
            for item in self.item:
                salary = item.unitary_value * item.finished
        elif self.c_type in ['Termino Indefinido', 'Prestacion de Servicios']:
            for bonus in self.bonus:
                salary += bonus.value
            return (self.base_salary + salary) * 0.92
        return self.base_salary + salary

    def sub_trans(self):
        '''Return the transportation allowance'''
        if self.c_type in ['Termino Indefinido', 'Prestacion de Servicios']\
                           and self.base_salary < 908526 * 2:
            return 106454
        return 0

    def vacations(self):
        '''Return the vacations payment'''
        if self.c_type in ['Termino Indefinido', 'Prestacion de Servicios']:
            return (self.base_salary * self.worked_weeks) / 104
        return 0

    def cesantias(self):
        '''Calculate the 'cesantias' '''
        if self.c_type in ['Termino Indefinido', 'Prestacion de Servicios']:
            return (self.base_salary * self.worked_weeks) / 52

    def in_cesantias(self):
        '''Calculate the 'cesantias' taxes'''
        if self.c_type in ['Termino Indefinido', 'Prestacion de Servicios']:
            return (self.base_salary * self.worked_weeks * 0.12) / 52
