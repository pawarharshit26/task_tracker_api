from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declared_attr
from app.db.base import Base
from datetime import datetime

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CreateModel:
    @declared_attr
    def creator_id(cls):
        return Column(Integer, ForeignKey('user.id'), nullable=True, comment='References the user who created this record')
    
    @declared_attr
    def creator(cls):
        return relationship(
            "User",
            foreign_keys=[cls.creator_id],
            remote_side="User.id"
        )


class UpdateModel:
    @declared_attr
    def updater_id(cls):
        return Column(Integer, ForeignKey('user.id'), nullable=True, comment='References the user who last updated this record')
    
    @declared_attr
    def updater(cls):
        return relationship(
            "User",
            foreign_keys=[cls.updater_id],
            remote_side="User.id"
        )


class DeleteModel:
    @declared_attr
    def deleted_at(cls):
        return Column(DateTime, nullable=True, comment='Timestamp when this record was soft-deleted')

    @declared_attr
    def deleter_id(cls):
        return Column(Integer, ForeignKey('user.id'), nullable=True, comment='References the user who deleted this record')
    
    @declared_attr
    def deleter(cls):
        return relationship(
            "User",
            foreign_keys=[cls.deleter_id],
            remote_side="User.id"
        )

class CreateUpdateDeleteModel(BaseModel, CreateModel, UpdateModel, DeleteModel):
    __abstract__ = True