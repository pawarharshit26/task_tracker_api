from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm._orm_constructors import relationship

from app.db.models.base import CreateModel, CreateUpdateDeleteModel


class User(CreateUpdateDeleteModel):
    __tablename__ = "user"

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
        comment="User's email address (must be unique)",
    )
    name = Column(String, nullable=False, comment="User's full name")
    password = Column(String, nullable=False, comment="Hashed password")
    is_active = Column(
        Boolean, default=True, comment="Whether the user account is active"
    )
    auth_token = relationship(
        "AuthToken",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}')>"


class AuthToken(CreateModel):
    __tablename__ = "auth_token"

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True)
    token = Column(String, nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="auth_token")

    def __repr__(self) -> str:
        return f"<AuthToken(id={self.id}, token='{self.user_id}')>"
