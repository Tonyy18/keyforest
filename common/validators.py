from django.core.validators import validate_email


def validate_email(mail):
    valid_email = False
    try:
        validate_email(mail)
        valid_email = True
    except validate_email.ValidationError:
        valid_email = False
    return valid_email