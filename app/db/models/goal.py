from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import CreateUpdateDeleteModel


class Goal(CreateUpdateDeleteModel):
    """
    Outcome-Oriented

    Examples:
        •	"Become senior backend engineer"
        •	"Perform flute recital confidently"

    Why
    •	Gives direction to effort
    •	Still abstract, not daily

    Rules
    •	Track can have multiple goals (but few active)
    •	Goals can overlap in time

    Long-form description lives in Block rows (owner_type="goal").
    """

    __tablename__ = "goal"

    track_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("track.id"), nullable=False
    )
    track = relationship("Track", back_populates="goals", foreign_keys=[track_id])

    title: Mapped[str] = mapped_column(String, nullable=False)
    horizon: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        doc="Free-form time horizon hint (e.g. '6 months', 'this year').",
    )

    phases: Mapped[list] = relationship(
        "Phase", back_populates="goal", foreign_keys="[Phase.goal_id]"
    )
