#!/usr/bin/python3 

'''
Admin class to manage the data of each company


Atributes:
    id = Auto increment number.
    username = Name of the user to login
    password_hash = encrypted password
    company_id = User Company


Methods:
    hash_password(password) = encrypt and storage the password
    verify_password(password) = validate if the passed password is a
                                valid one
    generate_auth_token(time) = generate an auth token that expire in 'time'
                                (seconds)
    verify_auth_token(token) = verify if the passed token is a valid one
'''

from models.basemodel import BaseModel, Base
import models
from api.app import app
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import generate_password_hash, check_password_hash


class Admin(BaseModel, Base):
    '''
Admin class definition.
'''

    __tablename__ = 'admin_user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(128), nullable=False)
    company_id = Column(ForeignKey('company.id'), nullable=False)
    company = relationship('Company', back_populates='admin_user')


    def hash_password(self, password):
        '''Encrypt and storage the password'''
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        '''Verify if the passed password is valid, Return a boolean'''
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=900):
        '''Generate a auth token to use the api, allow one argumet (seconds)'''
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        '''Verify if a token is valid, return a boolean'''
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        admin = models.storage.all(Admin).get(data['id'])
        return admin
