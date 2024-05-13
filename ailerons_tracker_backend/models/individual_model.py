""" Individual and Context models """
from typing import List
from sqlalchemy import Date, DateTime, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ailerons_tracker_backend.db import db
from ailerons_tracker_backend.models.picture_model import Picture


class Individual(db.Model):
    """ Model for an individual

    Attributes:
        id(int): ID, auto.
        created_at (timestamp): auto.
        common_name (str): auto.
        binomial_name (str): auto.
        icon (int): auto.
        individual_name (str): unique.
        sex (str)
        picture (PostgreSQL Array)
        description (str)
        context: relationship, doesn't appear in database but allow joins, back-populating and cascades.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)

    created_at: Mapped[Date] = mapped_column(DateTime, default=func.now())

    common_name: Mapped[str] = mapped_column(
        Text, default='Diable de mer méditerranéen')

    binomial_name: Mapped[str] = mapped_column(default='Mobula mobular')

    icon: Mapped[int] = mapped_column(default=1)

    individual_name: Mapped[str] = mapped_column(unique=True)

    sex: Mapped[str] = mapped_column(Text)

    description: Mapped[str] = mapped_column(Text)

    picture: Mapped[List['Picture']] = relationship(
        back_populates='individual',
        cascade="all"
    )

    context: Mapped['Context'] = relationship(
        back_populates='individual',
        cascade="all, delete-orphan"
    )
