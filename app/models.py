from enum import unique
from . import db,pwd_context
from datetime import datetime
import uuid
import base64
from .payment.verify_payment import Verify
from flask_login import UserMixin


#your models here
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    names = db.Column(db.String(1000), nullable=False)
    ref = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(200), unique=True)
    phone = db.Column(db.String(20), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    copies = db.Column(db.Integer,default=1)
    verified = db.Column(db.Boolean, default=False)


    def __init__(self,amount,names,email,phone) -> None:
        self.amount = amount
        self.names = names
        self.ref = base64.urlsafe_b64encode(str(uuid.uuid4()).encode()).decode('utf-8')
        self.email = email
        self.phone =phone
        self.date_created = datetime.utcnow()
        self.copies = 1
        self.verified = False

    def __str__(self) -> str:
        return f'<Payment {self.email}>'
    

    def verify_payment(self):
        response = Verify().verify_payment(self.ref)
        if response["status"] and response["data"]["amount"]/100 == self.amount:
            self.verified = True
            db.session.commit()
            return True
        return False

    @classmethod
    def payment_exists(cls,email,phone):
        if cls.query.filter_by(email=email).first() or cls.query.filter_by(phone=phone).first():
            return cls.query.filter_by(email=email).first()
        else:
            return None


class Admin(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(500), nullable=False)

    def __init__(self,username,password) -> None:
        self.username = username
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password) -> bool:
        return pwd_context.verify(password,self.password)

    def __str__(self) -> str:
        return f'<Admin {self.username}>'
    
