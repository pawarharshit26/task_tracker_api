from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import CreateUpdateDeleteModel


class Goal(CreateUpdateDeleteModel):
    """
    Outcome-Oriented

    Examples:
        •	“Become senior backend engineer”
        •	“Perform flute recital confidently”

    Why
    •	Gives direction to effort
    •	Still abstract, not daily

    Rules
    •	Track can have multiple goals (but few active)
    •	Goals can overlap in time
    """

    __tablename__ = "goal"

    track_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("track.id"), nullable=False
    )
    track = relationship("Track", back_populates="goals", foreign_keys=[track_id])
    # description lived in blocks

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text)

    phases: Mapped[list] = relationship(
        "Phase", back_populates="goal", foreign_keys="[Phase.goal_id]"
    )
