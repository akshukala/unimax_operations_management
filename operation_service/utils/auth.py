from django.contrib.auth.models import User
#from agroutils.exceptions.agro_error import AError
import re

from flask import session


class NotAuthenticatedException(Exception):
    pass

class InvalidPasswordError(Exception):
    '''
    Raised when a invalid password is provided.
    '''


def get_user():
    user_id = session.get('user_id')
    if not user_id:
        raise NotAuthenticatedException()

    return User.objects.get(id=session.get('user_id'))


def valid_password(password, min_length=6, max_length=20, match_re=()):
    '''
    Check for the validity of the provide password
    '''
    if not min_length <= len(password) <= max_length:
        return False

    return all(re.search(regex, password) for regex in match_re)


def valid_email(email):
    return bool(
        re.search(r'^[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,4}$', email)
    )
