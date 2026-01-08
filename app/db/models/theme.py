from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import CreateUpdateDeleteModel


class Theme(CreateUpdateDeleteModel):
    """
    Life Domain
    Theme represents a life domain under a Vision.

    Examples:
    •	Health
    •	Career
    •	Creativity
    •	Relationships

    Why
    •	Human brains don't manage 100 goals
    •	Themes group intention

    Rules
    •	3-6 active themes max
    •	Must belong to a Vision
    """

    __tablename__ = "theme"

    vision_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("vision.id"), nullable=False
    )
    vision = relationship("Vision", back_populates="themes", foreign_keys=[vision_id])

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    tracks = relationship(
        "Track", back_populates="theme", foreign_keys="[Track.theme_id]"
    )
