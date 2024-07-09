""" Record Model """

from uuid import UUID

from sqlalchemy import TIMESTAMP, ForeignKey, Integer, func
from sqlalchemy.types import Uuid
from ailerons_tracker_backend.models.record_field_model import LocalisationField, DepthField
from ailerons_tracker_backend.db import db
from sqlalchemy.orm import Mapped, mapped_column as mc, relationship as rel


class Record(db.Model):
    """ Model for a GPS data record. """
    id: Mapped[int] = mc(Integer, primary_key=True, unique=True)
    created_at: Mapped[str] = mc(TIMESTAMP, default=func.now())
    latitude: Mapped[int] = mc(Integer)
    longitude: Mapped[int] = mc(Integer)
    depth: Mapped[int] = mc(Integer)
    csv_uuid: Mapped[UUID] = mc(Uuid, ForeignKey('csv.uuid'))
    csv: Mapped['csv'] = rel(back_populates='csv', cascade='all')
    record_timestamp: Mapped[str] = mc(TIMESTAMP)

