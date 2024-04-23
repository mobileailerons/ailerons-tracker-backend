""" User model """

import os
from dotenv import load_dotenv
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ailerons_tracker_backend.errors import EnvVarError

load_dotenv()

pwd = os.getenv('ADMIN_PWD')

if not pwd:
    raise EnvVarError('ADMIN_PWD')


class User(UserMixin):
    """ Load the default version of User class provided by flask_login and add methods """

    pwd_hash = generate_password_hash(pwd)
    id = 'Admin'

    @ classmethod
    def check_pwd(cls, pwd):
        """ Compare stored and provided password hash """

        return check_password_hash(pwhash=cls.pwd_hash, password=pwd)
