from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError

from ..models import *


# your form class here
class PaymentForm(FlaskForm):
    names = StringField("full name",validators=[DataRequired(),Length(min=2,max=1000)])
    email = EmailField("email",validators=[Email(),DataRequired()])
    phone = StringField("phone", validators=[DataRequired()])

    def validate_phone(self,phone):
        if phone.data.startswith('+234') and (len(phone.data) < 14 or len(phone.data)>14):
            raise ValidationError('phone no is incorrect')
        if phone.data.startswith('0') and (len(phone.data) < 11 or len(phone.data)>11):
            raise ValidationError('phone no is incorrect')

