""" Article Model """
from sqlalchemy import Boolean, Identity, Text, func
from sqlalchemy.dialects import postgresql
from ailerons_tracker_backend.db import db

from sqlalchemy.orm import Mapped, mapped_column as mc


class Article(db.Model):
    """ Model for a news article.
    
    Args:
        title (str)
        content (str)
        publication_date (str)
        image_url (str)


    """
    id: Mapped[int] = mc(postgresql.BIGINT, Identity(
        start=1, always=True), primary_key=True, unique=True)

    created_at: Mapped[str] = mc(
        postgresql.TIMESTAMP(timezone=True), default=func.now())

    title: Mapped[str] = mc(Text)

    content: Mapped[str] = mc(Text)

    published: Mapped[bool] = mc(Boolean, default=False)

    archived: Mapped[bool] = mc(Boolean, default=False)

    publication_date: Mapped[str] = mc(postgresql.TIMESTAMP)

    image_url: Mapped[str] = mc(Text)
