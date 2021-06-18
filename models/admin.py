#!/usr/bin/python3 

'''Employee Class Definition'''

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
'''

    __tablename__ = 'admin_user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(128), nullable=False)
    company_id = Column(ForeignKey('company.id'), nullable=False)
    company = relationship('Company', back_populates='admin_user')


    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=900):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        admin = models.storage.all(Admin).get(data['id'])
        return admin
