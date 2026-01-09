from sqlalchemy import Boolean, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import CreateUpdateDeleteModel


class Phase(CreateUpdateDeleteModel):
    """
    Time-Boxed Focus
    Examples:
        •	“DSA Foundation - 8 weeks”
        •	“Flute basics - breath control”

    Why
    •	Humans need short horizons
    •	Prevents endless vague goals

    Rules
    •	Phase has start & end dates
    •	Only 1 active phase per goal (constraint)
    """

    __tablename__ = "phase"

    goal_id: Mapped[int] = mapped_column(Integer, ForeignKey("goal.id"), nullable=False)
    goal = relationship("Goal", back_populates="phases")

    title: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[Date] = mapped_column(Date)
    end_date: Mapped[Date] = mapped_column(Date)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    daily_commitments: Mapped[list] = relationship(
        "DailyCommitment", back_populates="phase"
    )
