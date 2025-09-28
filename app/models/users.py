from sqlmodel import SQLModel, Field, Column, String, Boolean, DateTime
from datetime import datetime
from typing import Optional


class User(SQLModel, table=True):
    __tablename__ = "users"  # <-- custom table name

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(50), nullable=False))
    email: str = Field(sa_column=Column(String, unique=True, nullable=False))
    password: str = Field(sa_column=Column(String, nullable=False))
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True, onupdate=datetime.now),
    )
    deleted_at: Optional[datetime] = Field(default=None)
    is_active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))
    is_superuser: bool = Field(default=False, sa_column=Column(Boolean, nullable=False))
