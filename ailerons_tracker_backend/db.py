""" SQLAlchemy DB interface """

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """ Base class that can be customized if needed """
    pass


db = SQLAlchemy(model_class=Base)
