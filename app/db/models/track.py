from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
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

    cadence_per_week: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        doc="Target sessions per week (1-7; 7 = daily). Null = no target.",
    )
    is_paused: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        doc="True = excluded from suggestions and cadence checks; data retained.",
    )
    paused_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        doc="When the track was last paused. Null when active.",
    )

    goals: Mapped[list] = relationship(
        "Goal", back_populates="track", foreign_keys="[Goal.track_id]"
    )
