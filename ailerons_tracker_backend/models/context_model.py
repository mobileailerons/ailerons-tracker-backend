""" Context model """
from sqlalchemy import Date, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ailerons_tracker_backend.db import db

# be careful not to cause circular imports when importing models that share a relationship in the same file
# import inside the function if you encounter issues


class Context(db.Model):
    """ Context model

    Attributes:
        id (int): auto.
        date (datestring): %Y/%m/%d.
        individual: relationship, doesn't appear but allow joins and back-populating.
        individual_id (int): foreign key.
        situation (str)
        size (int)
        behavior (str)

    """
    id: Mapped[int] = mapped_column(
        primary_key=True,
        unique=True)
    date: Mapped[Date] = mapped_column(
        DateTime,
        default=func.now())
    individual: Mapped['Individual'] = relationship(
        back_populates='context')
    individual_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('individual.id'))
    situation: Mapped[str] = mapped_column(Text)
    size: Mapped[int] = mapped_column(Integer)
    behavior: Mapped[str] = mapped_column(Text)
