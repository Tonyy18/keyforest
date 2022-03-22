from django.core.validators import validate_email
from . import parameters

def validate_email(mail):
    valid_email = False
    try:
        validate_email(mail)
        valid_email = True
    except validate_email.ValidationError:
        valid_email = False
    return valid_email

def app_name(name):
    return len(name) >= parameters.Application.min_name_length and len(name) <= parameters.Application.max_name_length

def license_name(name):
    return len(name) >= parameters.License.min_name_length and len(name) <= parameters.License.max_name_length