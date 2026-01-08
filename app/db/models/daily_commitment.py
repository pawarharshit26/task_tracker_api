from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

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
    phase_id = mapped_column(Integer, ForeignKey("phase.id"), nullable=False)
    phase = relationship("Phase", back_populates="daily_commitments")

    commitment_date = mapped_column(Date, nullable=False)
    intent = mapped_column(String, nullable=False)

    execution_log = relationship(
        "ExecutionLog", uselist=False, back_populates="commitment"
    )
