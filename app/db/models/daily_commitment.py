from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import CreateUpdateDeleteModel


class DailyCommitment(CreateUpdateDeleteModel):
    """
    Intent for a Day
    A promise you make before execution.

    Examples:
        •	“Practice flute 30 min”
        •	“Solve 2 DSA problems”

    Why it exists
    •	Separates intention from reality
    •	Without this, reflection is meaningless

    Rules
    •	Created at start of day (or day before)
        •	One commitment belongs to one Phase
        •	Can be skipped (but logged)
    """

    __tablename__ = "daily_commitment"
    phase_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("phase.id"), nullable=False
    )
    phase = relationship("Phase", back_populates="daily_commitments")

    commitment_date: Mapped[Date] = mapped_column(Date, nullable=False)
    intent: Mapped[str] = mapped_column(String, nullable=False)
    expected_minutes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        doc="Planned minutes for this commitment.",
    )
    mve_minutes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        doc="Minimum Viable Effort (frozen at write time): max(5, round(expected_minutes / 3)).",
    )

    execution_log = relationship(
        "ExecutionLog", uselist=False, back_populates="commitment"
    )
