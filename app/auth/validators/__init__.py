import re
from wtforms import ValidationError

def validate_lowercase(form, field):
    r = re.findall("/[a-z]/g", field.data)
    if r is None:
        raise ValidationError('Must have lowercase letter')

def validate_uppercase(form, field):
    r = re.findall("/[A-Z]/g", field.data)
    if r is None:
        raise ValidationError('Must have uppercase letter')

def special_character(form, field):
    r = re.findall('''/[`~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/]/''', field.data)
    if r is None:
        raise ValidationError('Must have special character')
