""" User model """

import os
from dotenv import load_dotenv
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()


class User(UserMixin):
    """ Load the default version of User class provided by flask_login and add methods """

    pwd_hash = generate_password_hash(os.getenv("ADMIN_PWD"))
    id = 'Admin'

    @classmethod
    def check_pwd(self, pwd):
        """ Compare stored and provided password hash """
        return check_password_hash(pwhash=self.pwd_hash, password=pwd)
