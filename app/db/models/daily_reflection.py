import enum

from sqlalchemy import Date, Enum, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import CreateUpdateDeleteModel


class Mood(str, enum.Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    NEUTRAL = "neutral"
    HIGH = "high"
    VERY_HIGH = "very_high"


class DailyReflection(CreateUpdateDeleteModel):
    """
    End-of-day reflection. Day-level mood + free-form blocks.

    Rules
    •	One row per (user_id, date)
    •	mood is optional (Mood enum)
    •	Long reflection content lives in Block rows (owner_type="daily_reflection")
    """

    __tablename__ = "daily_reflection"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", foreign_keys=[user_id])

    date: Mapped[Date] = mapped_column(Date, nullable=False)
    mood: Mapped[Mood | None] = mapped_column(
        Enum(Mood, name="mood"),
        nullable=True,
        doc="Subjective day mood: very_low | low | neutral | high | very_high.",
    )

    __table_args__ = (
        UniqueConstraint("user_id", "date", name="uq_daily_reflection_user_date"),
    )
