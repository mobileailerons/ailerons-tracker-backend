from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ailerons_tracker_backend.db import db


class Picture(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)

    url: Mapped[str] = mapped_column(Text)

    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())

    individual: Mapped['Individual'] = relationship(
        back_populates='picture', cascade='all')

    individual_id: Mapped[int] = mapped_column(ForeignKey('individual.id'))
