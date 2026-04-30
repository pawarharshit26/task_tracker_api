from sqlalchemy import CheckConstraint, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import CreateUpdateDeleteModel


class ExecutionLog(CreateUpdateDeleteModel):
    """
    What Actually Happened
    What actually happened — truth, not intention.

    Examples:
        •	"Practiced 12 minutes, distracted"
        •	"Did 1 problem, got stuck"

    Why it exists
    •	Reality check
    •	Prevents self-deception
    •	Enables learning

    Rules
    •	ExecutionLog belongs to DailyCommitment
    •	1-to-1 with DailyCommitment (commitment_id is unique)
    •	Plain factual fields (actual_minutes, energy_level, note);
        rich reflection lives in Block rows (owner_type="execution_log").
    """

    __tablename__ = "execution_log"
    commitment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("daily_commitment.id"), nullable=False, unique=True
    )
    commitment = relationship("DailyCommitment", back_populates="execution_log")

    actual_minutes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        doc="Actual minutes spent. Null = not yet logged.",
    )
    energy_level: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        doc="Subjective energy 1-5 during the session.",
    )
    note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Short factual note. Long reflection → blocks.",
    )

    __table_args__ = (
        CheckConstraint(
            "energy_level IS NULL OR (energy_level BETWEEN 1 AND 5)",
            name="ck_execution_log_energy_level_range",
        ),
    )
