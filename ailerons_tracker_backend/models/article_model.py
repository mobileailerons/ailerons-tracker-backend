""" Article Model """
from sqlalchemy import TIMESTAMP, Boolean, Integer, Text, func
from ailerons_tracker_backend.db import db

from sqlalchemy.orm import Mapped, mapped_column as mc


class Article(db.Model):
    """ Model for a news article. """
    id: Mapped[int] = mc(Integer, primary_key=True, unique=True)
    created_at: Mapped[str] = mc(TIMESTAMP, default=func.now())
    title: Mapped[str] = mc(Text)
    content: Mapped[str] = mc(Text)
    published: Mapped[bool] = mc(Boolean, default=False)
    archived: Mapped[bool] = mc(Boolean, default=False)
    publication_date: Mapped[str] = mc(TIMESTAMP)
    image_url: Mapped[str] = mc(Text)

