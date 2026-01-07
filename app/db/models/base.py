from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import declared_attr, relationship

from app.db.base import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)

class CreateModel(BaseModel):
    __abstract__ = True

    @declared_attr
    def created_at(cls):
        return Column(
            DateTime,
            nullable=False,
            default=datetime.utcnow,
            comment="Timestamp when this record was created",
        )

    @declared_attr
    def creator_id(cls):
        return Column(
            Integer,
            ForeignKey("user.id"),
            nullable=True,
            comment="References the user who created this record",
        )

    @declared_attr
    def creator(cls):
        return relationship(
            "User", foreign_keys=[cls.creator_id], remote_side="User.id"
        )


class UpdateModel(BaseModel):
    __abstract__ = True

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime,
            nullable=False,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
            comment="Timestamp when this record was updated",
        )

    @declared_attr
    def updater_id(cls):
        return Column(
            Integer,
            ForeignKey("user.id"),
            nullable=True,
            comment="References the user who last updated this record",
        )

    @declared_attr
    def updater(cls):
        return relationship(
            "User", foreign_keys=[cls.updater_id], remote_side="User.id"
        )


class DeleteModel(BaseModel):
    __abstract__ = True

    @declared_attr
    def deleted_at(cls):
        return Column(
            DateTime,
            nullable=True,
            comment="Timestamp when this record was deleted",
        )

    @declared_attr
    def deleter_id(cls):
        return Column(
            Integer,
            ForeignKey("user.id"),
            nullable=True,
            comment="References the user who deleted this record",
        )

    @declared_attr
    def deleter(cls):
        return relationship(
            "User", foreign_keys=[cls.deleter_id], remote_side="User.id"
        )


class CreateUpdateDeleteModel(CreateModel, UpdateModel, DeleteModel):
    __abstract__ = True
