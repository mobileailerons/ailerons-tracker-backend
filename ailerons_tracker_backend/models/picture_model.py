""" Picture model """
from sqlalchemy import ForeignKey, Identity, Text, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column as mc, relationship as rel
from ailerons_tracker_backend.db import db


class Picture(db.Model):
    """ Picture model
    Attributes: 
        id (int): primary key, unique.
        url (str): Cloudinary image url. 
        created_at (datetime): auto.
        individual (Individual): relationship.
        individual_id (int): foreign key. """

    id: Mapped[int] = mc(postgresql.BIGINT, Identity(
        start=1, always=True), primary_key=True, unique=True)

    created_at: Mapped[str] = mc(
        postgresql.TIMESTAMP(timezone=True), default=func.now())

    url: Mapped[str] = mc(Text)

    individual: Mapped['Individual'] = rel(
        back_populates='pictures')

    individual_id: Mapped[int] = mc(
        postgresql.BIGINT, ForeignKey('individual.id'))
