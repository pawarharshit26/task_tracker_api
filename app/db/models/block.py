from typing import Literal

from sqlalchemy import JSON, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import CreateUpdateDeleteModel


class Block(CreateUpdateDeleteModel):
    """
    Polymorphic content block for Notion-like editor.

    Attaches to:
        - Goal             (owner_type="goal")
        - Phase            (owner_type="phase")
        - ExecutionLog     (owner_type="execution_log")
        - DailyReflection  (owner_type="daily_reflection")

    Block types and their content shapes:
        paragraph   {"text": str}
        bullet      {"text": str}
        quote       {"text": str}
        heading     {"level": int (1-6), "text": str}
        checkbox    {"text": str, "checked": bool}

    No DB-level FK on owner_id — polymorphic ownership is enforced at
    the application layer (BlockService._verify_owner_exists).
    """

    __tablename__ = "block"

    owner_type: Mapped[
        Literal["goal", "phase", "execution_log", "daily_reflection"]
    ] = mapped_column(
        String,
        nullable=False,
        doc="Discriminator: 'goal' | 'phase' | 'execution_log' | 'daily_reflection'",
    )
    owner_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Integer PK of the owning record.",
    )
    block_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
        doc="Block type: paragraph | heading | bullet | checkbox | quote",
    )
    content: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        doc="Block content as JSON. Shape depends on block_type.",
    )
    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        doc="Zero-based ordering position within the owner's block list.",
    )

    __table_args__ = (Index("ix_block_owner_type_owner_id", "owner_type", "owner_id"),)
