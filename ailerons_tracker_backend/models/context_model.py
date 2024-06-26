""" Context model """

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column as mc, relationship as rel
from ailerons_tracker_backend.db import db
# be careful not to cause circular imports when importing models that share a rel in the same file
# import inside the function if you encounter issues


class Context(db.Model):
    """ Context model

    Attributes:
        id (int): auto.
        date (datestring): %Y/%m/%d.
        individual: relationship.
        individual_id (int): foreign key.
        situation (str)
        size (int)
        behavior (str) """

    id: Mapped[int] = mc(primary_key=True, unique=True)
    date: Mapped[Date] = mc(DateTime, default=func.now())
    individual: Mapped['Individual'] = rel(back_populates='context')
    individual_id: Mapped[int] = mc(Integer, ForeignKey('individual.id'))
    situation: Mapped[str] = mc(Text)
    size: Mapped[int] = mc(Integer)
    behavior: Mapped[str] = mc(Text)
