from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import CreateUpdateDeleteModel


class ExecutionLog(CreateUpdateDeleteModel):
    """
    What Actually Happened
    What actually happened — truth, not intention.

    Examples:
        •	“Practiced 12 minutes, distracted”
        •	“Did 1 problem, got stuck”

    Why it exists
    •	Reality check
    •	Prevents self-deception
    •	Enables learning

    Rules
    •	ExecutionLog belongs to DailyCommitment
    •	Can be empty or partial
    •	Immutable after day ends (later)
    """

    __tablename__ = "execution_log"
    commitment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("daily_commitment.id"), nullable=False, unique=True
    )
    commitment = relationship("DailyCommitment", back_populates="execution_log")

    actual_output: Mapped[str] = mapped_column(Text)
    reflection: Mapped[str] = mapped_column(Text)
