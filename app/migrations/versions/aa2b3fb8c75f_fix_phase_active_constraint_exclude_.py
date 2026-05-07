"""fix_phase_active_constraint_exclude_deleted

Revision ID: aa2b3fb8c75f
Revises: 764bbf3d4d80
Create Date: 2026-05-07 15:43:41.886015

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa2b3fb8c75f'
down_revision: Union[str, Sequence[str], None] = '764bbf3d4d80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index('ix_phase_one_active_per_goal', table_name='phase')
    op.create_index(
        'ix_phase_one_active_per_goal',
        'phase',
        ['goal_id'],
        unique=True,
        postgresql_where=sa.text("lifecycle = 'ACTIVE' AND deleted_at IS NULL"),
    )


def downgrade() -> None:
    op.drop_index('ix_phase_one_active_per_goal', table_name='phase')
    op.create_index(
        'ix_phase_one_active_per_goal',
        'phase',
        ['goal_id'],
        unique=True,
        postgresql_where=sa.text("lifecycle = 'ACTIVE'"),
    )
