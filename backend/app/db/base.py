from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import ORM models here so Alembic can detect metadata in later revisions.
