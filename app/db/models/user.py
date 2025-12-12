from sqlalchemy import Column, String, Boolean
from app.db.models.base import CreateUpdateDeleteModel


class User(CreateUpdateDeleteModel):
    __tablename__ = "users"
    
    email = Column(String, unique=True, index=True, nullable=False, comment="User's email address (must be unique)")
    name = Column(String, nullable=False, comment="User's full name")
    password = Column(String, nullable=False, comment="Hashed password")
    is_active = Column(Boolean, default=True, comment="Whether the user account is active")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}')>"
