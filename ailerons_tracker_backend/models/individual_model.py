""" Individual and Context models """

from typing import List
from sqlalchemy import Date, Identity, Text, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column as mc, relationship as rel
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
        description (str)
        picture: relationship, list of Picture entities.
        context: relationship, Context entity. """

    id: Mapped[int] = mc(
        postgresql.BIGINT, Identity(start=1, always=False), primary_key=True, unique=True)

    created_at: Mapped[Date] = mc(
        postgresql.TIMESTAMP(timezone=True), default=func.now())

    common_name: Mapped[str] = mc(
        Text, default='Diable de mer méditerranéen')

    binomial_name: Mapped[str] = mc(
        Text, default='Mobula mobular')

    individual_name: Mapped[str] = mc(
        Text, unique=True)

    sex: Mapped[str] = mc(Text)

    description: Mapped[str] = mc(Text)

    pictures: Mapped[List['Picture']] = rel(
        back_populates='individual', cascade='all, delete-orphan')

    context: Mapped['Context'] = rel(
        back_populates='individual', cascade="all, delete-orphan")

    records: Mapped[List['Record']] = rel(
        back_populates='individual', cascade='all, delete-orphan')

    point_features: Mapped[List['PointGeojson']] = rel(
        back_populates='individual', cascade='all, delete-orphan')

    feature_collection: Mapped[str] = mc(postgresql.JSON, nullable=True)

    line_feature: Mapped['LineGeojson'] = rel(
        back_populates='individual', cascade='all, delete-orphan')

    csv: Mapped['Csv'] = rel(
        back_populates='individual', cascade='all, delete-orphan')
