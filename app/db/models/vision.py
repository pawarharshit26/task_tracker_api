from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm._orm_constructors import relationship

from app.db.models.base import CreateUpdateDeleteModel


class Vision(CreateUpdateDeleteModel):
    """
    Identity Anchor
    Vision represents the user's long-term identity and life direction. It provides meaning and context to all goals below it.

    Why it exists
        •	To anchor why anything exists at all
        •	Rarely changes
        •	Not operational

    Constraints
    •	Only one active vision at a time
    •	Editable but versioned later if needed

    Does NOT
    •	Own tasks
    •	Track progress
    """

    __tablename__ = "vision"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=False, unique=True
    )
    user = relationship("User", back_populates="vision", foreign_keys=[user_id])

    title: Mapped[str] = mapped_column(
        String, nullable=False, doc="Short name of the vision."
    )
    description: Mapped[str] = mapped_column(
        Text, nullable=False, doc="Detailed articulation of the life vision."
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        doc="Whether the vision is active or not.",
    )

    themes = relationship(
        "Theme", back_populates="vision", foreign_keys="[Theme.vision_id]"
    )
