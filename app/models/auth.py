from sqlmodel import SQLModel, Field, Column, DateTime, String, Enum
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Relationship
from app.models.users import User
from enum import Enum as PyEnum


class TokenType(str, PyEnum):
    BEARER = "Bearer"


class Token(SQLModel, table=True):
    __tablename__ = "tokens"
    id: Optional[int] = Field(default=None, primary_key=True)
    token: str = Field(sa_column=Column(String, nullable=False))
    token_type: TokenType = Field(
        sa_column=Column(Enum(TokenType, name="token_type_enum"), nullable=False),
        default=TokenType.BEARER,
    )
    user_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    user: Optional[User] = Relationship(back_populates="tokens")
