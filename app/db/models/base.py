from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CreateModel(BaseModel):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.utcnow)
    creator_id = Column(Integer, ForeignKey('user.id'), nullable=True, comment='References the user who created this record')
    creator = relationship(
        "User",
        foreign_keys=["creator_id"],
        remote_side="User.id"
    )


class UpdateModel(BaseModel):
    __abstract__ = True
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    updater_id = Column(Integer, ForeignKey('user.id'), nullable=True, comment='References the user who last updated this record')
    updater = relationship(
        "User",
        foreign_keys=["updater_id"],
        remote_side="User.id"
    )


class DeleteModel(BaseModel):
    __abstract__ = True
    deleted_at = Column(DateTime, nullable=True, comment='Timestamp when this record was soft-deleted')
    deleter_id = Column(Integer, ForeignKey('user.id'), nullable=True, comment='References the user who deleted this record')
    deleter = relationship(
        "User",
        foreign_keys=["deleter_id"],
        remote_side="User.id"
    )

class CreateUpdateDeleteModel(BaseModel, CreateModel, UpdateModel, DeleteModel):
    __abstract__ = True 