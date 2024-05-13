""" Picture model """
from sqlalchemy import DateTime, ForeignKey, Text, func
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

    id: Mapped[int] = mc(primary_key=True, unique=True)
    url: Mapped[str] = mc(Text)
    created_at: Mapped[str] = mc(DateTime, default=func.now())
    individual: Mapped['Individual'] = rel(back_populates='picture',
                                           cascade='all')
    individual_id: Mapped[int] = mc(ForeignKey('individual.id'))
