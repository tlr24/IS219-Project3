import re
from wtforms import ValidationError
#from flask import flash

def validate_lowercase(form, field):
    r = re.findall("[a-z]", field.data)
    if len(r) is 0:
        raise ValidationError('Must have lowercase letter')

def validate_uppercase(form, field):
    r = re.findall("[A-Z]", field.data)
    if len(r) is 0:
        raise ValidationError('Must have uppercase letter')

def special_character(form, field):
    r = re.findall('''[`~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/]''', field.data)
    if len(r) is 0:
        raise ValidationError('Must have special character')
