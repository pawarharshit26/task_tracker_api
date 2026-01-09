from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import CreateUpdateDeleteModel


class Track(CreateUpdateDeleteModel):
    """
    Skill / Focus Area
    Track represents a life domain under a Theme.
    Examples:
        •	Backend Engineering
        •	Flute Practice
        •	Applied AI
        •	System Design Interviews

    Why
        •	Themes are too broad to execute
        •	Tracks are workable lanes

    Rules
    •	Track belongs to ONE Theme
    •	Can be paused
    •	Has its own cadence
    """

    __tablename__ = "track"

    theme_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("theme.id"), nullable=False
    )
    theme = relationship("Theme", back_populates="tracks", foreign_keys=[theme_id])

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    goals: Mapped[list] = relationship(
        "Goal", back_populates="track", foreign_keys="[Goal.track_id]"
    )
